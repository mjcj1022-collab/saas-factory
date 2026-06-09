"""
Factory Boy factories for test data generation.
"""
import factory
import factory.django
from django.utils import timezone


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "organizations.Organization"

    name = factory.Sequence(lambda n: f"Org {n}")
    slug = factory.Sequence(lambda n: f"org-{n}")
    plan = "starter"
    is_active = True


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "organizations.User"

    username = factory.Sequence(lambda n: f"user{n}@test.com")
    email = factory.LazyAttribute(lambda o: o.username)
    first_name = "Test"
    last_name = factory.Sequence(lambda n: f"User{n}")
    organization = factory.SubFactory(OrganizationFactory)
    role = "member"

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_user(*args, **kwargs)


# ── RFP ───────────────────────────────────────────────────────────────────────

class KnowledgeDocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "rfp.KnowledgeDocument"

    organization_id = factory.LazyAttribute(lambda o: factory.SubFactory(OrganizationFactory).id)
    title = factory.Sequence(lambda n: f"Policy Doc {n}")
    content = "This document covers security, access control, encryption, and MFA policies."
    doc_type = "policy"


class RFPRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "rfp.RFPRequest"

    organization_id = factory.LazyFunction(lambda: OrganizationFactory().id)
    title = factory.Sequence(lambda n: f"RFP Request {n}")
    status = "uploaded"


class RFPSectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "rfp.RFPSection"

    rfp = factory.SubFactory(RFPRequestFactory)
    heading = "Security"
    question = "Describe your MFA implementation."
    sequence = factory.Sequence(lambda n: n)


# ── Fleet ─────────────────────────────────────────────────────────────────────

class VehicleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "fleet.Vehicle"

    organization_id = factory.LazyFunction(lambda: OrganizationFactory().id)
    vin = factory.Sequence(lambda n: f"1HGBH41JXMN{n:06d}")
    make = "Ford"
    model = "F-150"
    year = 2022
    vehicle_type = "truck"
    odometer = 45000


class TelemetryEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "fleet.TelemetryEvent"

    vehicle = factory.SubFactory(VehicleFactory)
    code = "P0300"
    description = "Random Misfire"
    severity = "critical"
    payload = {}
    timestamp = factory.LazyFunction(timezone.now)


class WorkOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "fleet.WorkOrder"

    vehicle = factory.SubFactory(VehicleFactory)
    status = "open"
    description = "Oil change and filter replacement"
    estimated_cost = "149.99"


# ── Construction ──────────────────────────────────────────────────────────────

class ConstructionProjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "construction.Project"

    organization_id = factory.LazyFunction(lambda: OrganizationFactory().id)
    name = factory.Sequence(lambda n: f"Project {n}")
    address = "123 Main St, Dallas TX"
    status = "active"


# ── Franchise ─────────────────────────────────────────────────────────────────

class FranchiseBrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "franchise.FranchiseBrand"

    organization_id = factory.LazyFunction(lambda: OrganizationFactory().id)
    name = factory.Sequence(lambda n: f"Brand {n}")
    industry = "food_service"


class FranchiseeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "franchise.Franchisee"

    brand = factory.SubFactory(FranchiseBrandFactory)
    full_name = factory.Sequence(lambda n: f"Franchisee {n}")
    email = factory.Sequence(lambda n: f"franchisee{n}@test.com")
    status = "applicant"


# ── Hospitality ───────────────────────────────────────────────────────────────

class RentalPropertyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "hospitality.RentalProperty"

    organization_id = factory.LazyFunction(lambda: OrganizationFactory().id)
    name = factory.Sequence(lambda n: f"Property {n}")
    address = "456 Beach Rd, Miami FL"
    wifi_password = "testpass123"
    check_in_instructions = "Key lockbox code is 1234."


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "hospitality.Reservation"

    property = factory.SubFactory(RentalPropertyFactory)
    platform = "airbnb"
    guest_name = factory.Sequence(lambda n: f"Guest {n}")
    guest_email = factory.Sequence(lambda n: f"guest{n}@test.com")
    check_in = factory.LazyFunction(lambda: timezone.now())
    check_out = factory.LazyFunction(lambda: timezone.now().replace(hour=timezone.now().hour + 3))
    status = "confirmed"
