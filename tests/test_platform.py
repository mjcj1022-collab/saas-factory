"""
SaaS Factory — test suite.
Run: pytest
"""
import pytest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


# ─── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def org():
    from tests.factories import OrganizationFactory
    return OrganizationFactory()


@pytest.fixture
def user(org):
    from tests.factories import UserFactory
    return UserFactory(organization=org)


@pytest.fixture
def auth_client(user):
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


# ─── Organizations ────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestOrganizations:

    def test_register(self):
        client = APIClient()
        response = client.post("/api/auth/register/", {
            "email": "newuser@company.com",
            "password": "securepass123",
            "first_name": "John",
            "last_name": "Doe",
            "organization_name": "Acme Corp",
        }, format="json")
        assert response.status_code == 201
        assert "token" in response.data
        assert response.data["user"]["email"] == "newuser@company.com"

    def test_login(self, user):
        client = APIClient()
        user.set_password("testpass123")
        user.save()
        response = client.post("/api/auth/login/", {
            "email": user.email,
            "password": "testpass123",
        }, format="json")
        assert response.status_code == 200
        assert "token" in response.data

    def test_me(self, auth_client, user):
        response = auth_client.get("/api/auth/users/me/")
        assert response.status_code == 200
        assert response.data["email"] == user.email

    def test_unauthenticated_blocked(self):
        client = APIClient()
        response = client.get("/api/auth/users/me/")
        assert response.status_code == 401


# ─── RFP ─────────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestRFP:

    def test_create_rfp(self, auth_client, user, tmp_path):
        from unittest.mock import patch
        f = tmp_path / "test_rfp.pdf"
        f.write_bytes(b"%PDF-1.4 fake content")
        with patch("apps.rfp.tasks.parse_rfp_task.delay"):
            with open(f, "rb") as fh:
                response = auth_client.post("/api/rfp/requests/", {
                    "title": "Q3 RFP — Acme Corp",
                    "original_file": fh,
                }, format="multipart")
        assert response.status_code == 201
        assert response.data["status"] == "uploaded"

    def test_list_rfps_scoped_to_org(self, auth_client, user):
        from tests.factories import RFPRequestFactory, OrganizationFactory
        # Create RFP in same org
        RFPRequestFactory(organization_id=user.organization_id)
        # Create RFP in different org (should not appear)
        other_org = OrganizationFactory()
        RFPRequestFactory(organization_id=other_org.id)

        response = auth_client.get("/api/rfp/requests/")
        assert response.status_code == 200
        results = response.data.get("results", response.data)
        assert len(results) == 1

    def test_knowledge_upload(self, auth_client, tmp_path):
        from unittest.mock import patch
        f = tmp_path / "policy.pdf"
        f.write_bytes(b"%PDF-1.4 security policy content")
        with patch("apps.rfp.tasks.create_embeddings_task.delay"):
            with open(f, "rb") as fh:
                response = auth_client.post("/api/rfp/knowledge/", {
                    "title": "Security Policy",
                    "file": fh,
                    "doc_type": "policy",
                }, format="multipart")
        assert response.status_code == 201


@pytest.mark.django_db
class TestRFPServices:

    def test_compliance_engine_detects_gaps(self):
        from apps.rfp.services import ComplianceEngine
        engine = ComplianceEngine()
        question = "Describe your HIPAA compliance and PHI data handling procedures."
        answer = "We follow best practices for data security."
        gaps = engine.scan(question, answer)
        assert len(gaps) > 0
        frameworks = [g["framework"] for g in gaps]
        assert "hipaa" in frameworks

    def test_compliance_engine_clean_response(self):
        from apps.rfp.services import ComplianceEngine
        engine = ComplianceEngine()
        question = "Describe your audit logging."
        answer = "Our ISMS includes audit logs, risk assessments, and incident management per ISO 27001."
        gaps = engine.scan(question, answer)
        # Well-covered response should have fewer or no gaps
        critical = [g for g in gaps if g["severity"] == "critical"]
        assert len(critical) == 0


# ─── Fleet ───────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestFleet:

    def test_create_vehicle(self, auth_client, user):
        response = auth_client.post("/api/fleet/vehicles/", {
            "vin": "1HGBH41JXMN109186",
            "make": "Ford",
            "model": "F-150",
            "year": 2022,
            "vehicle_type": "truck",
            "odometer": 45000,
        }, format="json")
        assert response.status_code == 201

    def test_list_vehicles_org_scoped(self, auth_client, user):
        from tests.factories import VehicleFactory, OrganizationFactory
        VehicleFactory(organization_id=user.organization_id)
        VehicleFactory(organization_id=OrganizationFactory().id)  # other org
        response = auth_client.get("/api/fleet/vehicles/")
        results = response.data.get("results", response.data)
        assert len(results) == 1

    def test_fleet_health_endpoint(self, auth_client, user):
        from tests.factories import VehicleFactory
        VehicleFactory.create_batch(3, organization_id=user.organization_id)
        response = auth_client.get("/api/fleet/vehicles/fleet_health/")
        assert response.status_code == 200
        assert "total" in response.data
        assert response.data["total"] == 3


@pytest.mark.django_db
class TestPredictiveMaintenance:

    def test_mileage_based_prediction(self):
        from tests.factories import VehicleFactory
        from apps.fleet.services import PredictiveMaintenanceEngine
        vehicle = VehicleFactory(odometer=30050)
        engine = PredictiveMaintenanceEngine()
        predictions = engine.analyze(str(vehicle.id))
        components = [p["component"] for p in predictions]
        assert "Transmission Fluid" in components

    def test_fault_code_prediction(self):
        from tests.factories import VehicleFactory, TelemetryEventFactory
        from apps.fleet.services import PredictiveMaintenanceEngine
        vehicle = VehicleFactory()
        # Add multiple P0300 events to trigger high confidence
        TelemetryEventFactory.create_batch(5, vehicle=vehicle, code="P0300")
        engine = PredictiveMaintenanceEngine()
        predictions = engine.analyze(str(vehicle.id))
        critical = [p for p in predictions if p.get("severity") == "critical"]
        assert len(critical) >= 1
        assert any("Misfire" in p["component"] for p in critical)


# ─── Construction ────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestConstruction:

    def test_create_project(self, auth_client):
        response = auth_client.post("/api/construction/projects/", {
            "name": "Downtown Office Tower",
            "address": "100 Main St, Dallas TX",
            "status": "planning",
        }, format="json")
        assert response.status_code == 201
        assert response.data["name"] == "Downtown Office Tower"

    def test_project_org_scoped(self, auth_client, user):
        from tests.factories import ConstructionProjectFactory, OrganizationFactory
        ConstructionProjectFactory(organization_id=user.organization_id)
        ConstructionProjectFactory(organization_id=OrganizationFactory().id)
        response = auth_client.get("/api/construction/projects/")
        results = response.data.get("results", response.data)
        assert len(results) == 1


# ─── Franchise ───────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestFranchise:

    def test_create_brand(self, auth_client):
        response = auth_client.post("/api/franchise/brands/", {
            "name": "BurgerCo",
            "industry": "food_service",
            "royalty_rate": "6.00",
        }, format="json")
        assert response.status_code == 201

    def test_pipeline_endpoint(self, auth_client, user):
        from tests.factories import FranchiseBrandFactory, FranchiseeFactory
        from apps.franchise.models import FranchiseLocation
        brand = FranchiseBrandFactory(organization_id=user.organization_id)
        franchisee = FranchiseeFactory(brand=brand)
        FranchiseLocation.objects.create(
            franchisee=franchisee,
            address="123 Oak St",
            launch_status="construction",
        )
        response = auth_client.get("/api/franchise/locations/pipeline/")
        assert response.status_code == 200
        assert "construction" in response.data


# ─── Hospitality ─────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestHospitality:

    def test_ai_messaging_wifi(self):
        from tests.factories import ReservationFactory
        from apps.hospitality.services import GuestMessagingAI
        reservation = ReservationFactory()
        ai = GuestMessagingAI()
        response = ai.classify_and_respond("What's the wifi password?", reservation)
        assert "testpass123" in response

    def test_ai_messaging_checkin(self):
        from tests.factories import ReservationFactory
        from apps.hospitality.services import GuestMessagingAI
        reservation = ReservationFactory()
        ai = GuestMessagingAI()
        response = ai.classify_and_respond("How do I check in?", reservation)
        assert "1234" in response  # lockbox code from factory

    def test_smart_lock_create(self):
        from tests.factories import ReservationFactory
        from apps.hospitality.services import SmartLockManager
        from apps.hospitality.models import SmartLockCode
        reservation = ReservationFactory()
        manager = SmartLockManager()
        code = manager.create_code(reservation)
        assert len(code) == 6
        assert code.isdigit()
        lock = SmartLockCode.objects.get(reservation=reservation)
        assert lock.created is True

    def test_cleaning_dispatch(self):
        from tests.factories import ReservationFactory
        from apps.hospitality.services import CleaningDispatcher
        from apps.hospitality.models import CleaningJob
        reservation = ReservationFactory()
        dispatcher = CleaningDispatcher()
        dispatcher.dispatch_after_checkout(reservation)
        job = CleaningJob.objects.get(reservation=reservation)
        assert job.status == "scheduled"
        assert len(job.checklist) > 0


# ─── Event Bus ───────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestEventBus:

    def test_event_publish(self, org):
        from core.events.models import EventPublisher, DomainEvent
        event = EventPublisher.publish(
            event_type="rfp.uploaded",
            aggregate_type="RFPRequest",
            aggregate_id="test-123",
            payload={"rfp_id": "test-123"},
            organization_id=org.id,
        )
        assert DomainEvent.objects.filter(id=event.id).exists()
        assert event.event_type == "rfp.uploaded"

    def test_event_router_registration(self):
        from core.events.models import EventRouter
        calls = []
        EventRouter.register("test.event", lambda e: calls.append(e))

        from core.events.models import DomainEvent
        import uuid
        fake_event = DomainEvent(
            id=uuid.uuid4(),
            event_type="test.event",
            organization_id=uuid.uuid4(),
            aggregate_type="Test",
            aggregate_id="1",
            payload={},
        )
        EventRouter.route(fake_event)
        assert len(calls) == 1


# ─── Workflow Engine ─────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestWorkflowEngine:

    def test_workflow_creation(self, auth_client, user):
        response = auth_client.post("/api/platform/workflows/", {
            "name": "RFP Upload Notification",
            "description": "Notify team when RFP is uploaded",
            "is_active": True,
        }, format="json")
        assert response.status_code == 201
        assert response.data["name"] == "RFP Upload Notification"

    def test_workflow_executor_with_notification(self, org):
        from core.workflows.models import Workflow, WorkflowTrigger, WorkflowAction
        from core.workflows.executor import WorkflowExecutor
        from core.events.models import DomainEvent
        from core.notifications.models import Notification
        import uuid

        wf = Workflow.objects.create(
            organization_id=org.id,
            name="Test Notification Workflow",
            is_active=True,
        )
        WorkflowTrigger.objects.create(workflow=wf, event_type="rfp.uploaded")
        WorkflowAction.objects.create(
            workflow=wf,
            sequence=1,
            action_type="send_notification",
            config={
                "channel": "email",
                "recipient": "team@company.com",
                "subject": "RFP uploaded",
                "message": "New RFP: {rfp_id}",
            },
        )

        event = DomainEvent(
            id=uuid.uuid4(),
            organization_id=org.id,
            event_type="rfp.uploaded",
            aggregate_type="RFPRequest",
            aggregate_id="rfp-1",
            payload={"rfp_id": "rfp-1"},
        )
        executions = WorkflowExecutor.run_for_event(event)
        assert len(executions) == 1
        assert executions[0].status == "completed"
        notif = Notification.objects.filter(organization_id=org.id).last()
        assert notif is not None
        assert "rfp-1" in notif.message


# ─── Billing ─────────────────────────────────────────────────────────────────

@pytest.mark.django_db
class TestBilling:

    def test_current_subscription_no_sub(self, auth_client):
        response = auth_client.get("/api/platform/billing/subscriptions/current/")
        assert response.status_code == 200
        assert response.data["status"] == "none"

    def test_subscription_scoped_to_org(self, auth_client, user):
        from core.billing.models import Subscription
        from tests.factories import OrganizationFactory
        Subscription.objects.create(organization_id=user.organization_id, plan="growth", status="active")
        Subscription.objects.create(organization_id=OrganizationFactory().id, plan="enterprise", status="active")
        response = auth_client.get("/api/platform/billing/subscriptions/")
        results = response.data.get("results", response.data)
        assert len(results) == 1
        assert results[0]["plan"] == "growth"
