/// <reference types="vite/client" />

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

interface ImportMetaEnv {
  readonly VITE_API_URL?: string;
}

declare module "*.css" {
  const content: Record<string, string>;
  export default content;
}
