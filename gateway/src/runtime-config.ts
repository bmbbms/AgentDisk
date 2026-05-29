export interface GatewayRuntimeConfig {
  gatewayPort: number;
  gatewayPublicUrl: string;
  webBaseUrl: string;
  defaultAgentEndpoint: string;
  oauthClientId: string;
  oauthClientSecret: string;
  oauthRedirectUris: string[];
  oauthDefaultRedirectUri: string;
  oauthScopes: string[];
  oauthAuthorizeUrl: string;
  oauthTokenUrl: string;
  oauthUserInfoUrl: string;
}

const DEFAULT_GATEWAY_PORT = 3100;
const DEFAULT_WEB_BASE_URL = 'http://localhost:9101';
const DEFAULT_AGENT_ENDPOINT = 'http://localhost:8090/process';
const DEFAULT_BACKEND_CALLBACK_URL = 'http://localhost:9100/auth/callback';

function parsePort(value: string | undefined, fallback: number): number {
  if (!value) {
    return fallback;
  }

  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function parseList(value: string | undefined, fallback: string[]): string[] {
  if (!value) {
    return fallback;
  }

  const items = value
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);

  return items.length > 0 ? items : fallback;
}

function normalizeBaseUrl(value: string | undefined, fallback: string): string {
  const candidate = value?.trim() || fallback;

  try {
    return new URL(candidate).toString().replace(/\/$/, '');
  } catch {
    return fallback;
  }
}

function normalizeUrl(value: string | undefined, fallback: string): string {
  const candidate = value?.trim() || fallback;

  try {
    return new URL(candidate).toString();
  } catch {
    return fallback;
  }
}

export function getGatewayRuntimeConfig(): GatewayRuntimeConfig {
  const gatewayPort = parsePort(process.env.GATEWAY_PORT, DEFAULT_GATEWAY_PORT);
  const gatewayPublicUrl = normalizeBaseUrl(
    process.env.GATEWAY_PUBLIC_URL,
    `http://localhost:${gatewayPort}`,
  );
  const webBaseUrl = normalizeBaseUrl(process.env.GATEWAY_WEB_URL, DEFAULT_WEB_BASE_URL);
  const defaultAgentEndpoint = normalizeUrl(
    process.env.GATEWAY_DEFAULT_AGENT_ENDPOINT,
    DEFAULT_AGENT_ENDPOINT,
  );
  const oauthRedirectUris = parseList(process.env.GATEWAY_OAUTH_REDIRECT_URIS, [
    `${webBaseUrl}/auth/callback`,
    DEFAULT_BACKEND_CALLBACK_URL,
  ]);
  const oauthDefaultRedirectUri = normalizeUrl(
    process.env.GATEWAY_OAUTH_DEFAULT_REDIRECT_URI,
    oauthRedirectUris[0],
  );
  const oauthClientId = process.env.GATEWAY_OAUTH_CLIENT_ID?.trim() || 'agentdisk';
  const oauthClientSecret = process.env.GATEWAY_OAUTH_CLIENT_SECRET?.trim() || 'agentdisk-secret';
  const oauthScopes = parseList(process.env.GATEWAY_OAUTH_SCOPES, ['openid', 'profile']);

  return {
    gatewayPort,
    gatewayPublicUrl,
    webBaseUrl,
    defaultAgentEndpoint,
    oauthClientId,
    oauthClientSecret,
    oauthRedirectUris,
    oauthDefaultRedirectUri,
    oauthScopes,
    oauthAuthorizeUrl: `${gatewayPublicUrl}/oauth2/authorize`,
    oauthTokenUrl: `${gatewayPublicUrl}/oauth2/token`,
    oauthUserInfoUrl: `${gatewayPublicUrl}/oauth2/userinfo`,
  };
}
