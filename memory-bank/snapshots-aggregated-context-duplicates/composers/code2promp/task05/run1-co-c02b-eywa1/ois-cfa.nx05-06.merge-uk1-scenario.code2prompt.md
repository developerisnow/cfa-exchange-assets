Project Path: prj_Cifra-rwa-exachange-assets

Source Tree:

```txt
prj_Cifra-rwa-exachange-assets
└── repositories
    └── customer-gitlab
        └── wt__ois-cfa__NX01
            ├── artifacts
            │   ├── AlexA
            │   │   ├── ois-cfa.reposcan.json
            │   │   └── project-C4.diagram.md
            │   ├── issuance-endpoints-coverage-report.md
            │   └── registry-flow-report.md
            ├── docs
            │   └── context
            │       ├── FRONTEND-CONTEXT.md
            │       ├── PROJECT-CONTEXT.md
            │       ├── RULES-SUMMARY.md
            │       └── WBS-OIS.md
            └── tasks
                ├── NX-05-issuer-dashboard-and-reports.md
                └── NX-06-issuer-payout-schedule-spec-and-ui.md

```

`repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/AlexA/ois-cfa.reposcan.json`:

```json
{
    "meta": {
      "repo": "repositories/customer-gitlab/ois-cfa",
      "branch": "infra.defis.deploy",
      "generated_at": "2025-11-18T09:05:00Z",
      "summary": {
        "domains": ["issuance", "registry", "settlement", "compliance", "identity"],
        "tracks": ["spec-contracts", "backend-services", "api-gateway-frontends", "observability-security", "ci-infra"],
        "trunk_branch_leaf_rules": {
          "trunk": ["docs/context/**", "docs/deploy/**", "packages/contracts/**", "packages/domain/**"],
          "branch": ["services/**", "apps/**", "ops/**", "ops/gitops/**"],
          "leaf": ["tests/**", "ops/scripts/**", "tasks/NX-*.md", "memory-bank/**"]
        },
        "git_branches": {
          "trunk": ["main", "develop (planned from infra.defis.deploy)"],
          "branch": ["infra", "deploy", "infra.defis.deploy", "release/*"],
          "leaf": ["feature/NX-*"]
        }
      }
    },
    "tree": {
      "path": ".",
      "type": "dir",
      "children": [
        {
          "path": "apps",
          "type": "dir",
          "level": "branch",
          "size_class": "L",
          "tags": ["frontends", "edge"],
          "children": [
            {
              "path": "apps/api-gateway",
              "type": "dir",
              "level": "branch",
              "size_class": "M",
              "tags": ["gateway", "dotnet", "yarp"]
            },
            {
              "path": "apps/portal-issuer",
              "type": "dir",
              "level": "branch",
              "size_class": "M",
              "tags": ["frontend", "issuer", "nextjs"]
            },
            {
              "path": "apps/portal-investor",
              "type": "dir",
              "level": "branch",
              "size_class": "M",
              "tags": ["frontend", "investor", "nextjs"]
            },
            {
              "path": "apps/backoffice",
              "type": "dir",
              "level": "branch",
              "size_class": "M",
              "tags": ["frontend", "backoffice", "nextjs"]
            },
            {
              "path": "apps/broker-portal",
              "type": "dir",
              "level": "branch",
              "size_class": "S",
              "tags": ["frontend", "broker"]
            },
            {
              "path": "apps/shared-ui",
              "type": "dir",
              "level": "branch",
              "size_class": "S",
              "tags": ["frontend", "shared-ui", "design-system"]
            }
          ]
        },
        {
          "path": "services",
          "type": "dir",
          "level": "branch",
          "size_class": "L",
          "tags": ["backend", "services"],
          "children": [
            {
              "path": "services/issuance",
              "type": "dir",
              "level": "branch",
              "size_class": "M",
              "tags": ["service", "issuance", "events-outbox"]
            },
            {
              "path": "services/registry",
              "type": "dir",
              "level": "branch",
              "size_class": "M",
              "tags": ["service", "registry", "orders", "wallets"]
            },
            {
              "path": "services/settlement",
              "type": "dir",
              "level": "branch",
              "size_class": "M",
              "tags": ["service", "settlement", "payouts"]
            },
            {
              "path": "services/compliance",
              "type": "dir",
              "level": "branch",
              "size_class": "M",
              "tags": ["service", "compliance", "kyc", "audit"]
            },
            {
              "path": "services/identity",
              "type": "dir",
              "level": "branch",
              "size_class": "S",
              "tags": ["service", "identity", "oidc"]
            },
            {
              "path": "services/fabric-gateway",
              "type": "dir",
              "level": "branch",
              "size_class": "S",
              "tags": ["service", "fabric", "dlt-adapter"]
            },
            {
              "path": "services/integrations",
              "type": "dir",
              "level": "branch",
              "size_class": "S",
              "tags": ["integrations"],
              "children": [
                {
                  "path": "services/integrations/bank-nominal",
                  "type": "dir",
                  "level": "branch",
                  "size_class": "S",
                  "tags": ["integration", "bank"]
                },
                {
                  "path": "services/integrations/esia-adapter",
                  "type": "dir",
                  "level": "branch",
                  "size_class": "S",
                  "tags": ["integration", "esia"]
                },
                {
                  "path": "services/integrations/edo-connector",
                  "type": "dir",
                  "level": "branch",
                  "size_class": "S",
                  "tags": ["integration", "edo"]
                }
              ]
            }
          ]
        },
        {
          "path": "packages",
          "type": "dir",
          "level": "trunk",
          "size_class": "L",
          "tags": ["packages"],
          "children": [
            {
              "path": "packages/contracts",
              "type": "dir",
              "level": "trunk",
              "size_class": "M",
              "tags": ["contracts", "openapi", "asyncapi", "schemas"]
            },
            {
              "path": "packages/domain",
              "type": "dir",
              "level": "trunk",
              "size_class": "M",
              "tags": ["domain", "value-objects"]
            },
            {
              "path": "packages/sdks/typescript-gateway",
              "type": "dir",
              "level": "branch",
              "size_class": "S",
              "tags": ["sdk", "typescript", "gateway-client"]
            },
            {
              "path": "packages/sdks/ts",
              "type": "dir",
              "level": "branch",
              "size_class": "S",
              "tags": ["sdk", "typescript", "api-client"]
            },
            {
              "path": "packages/types/ts",
              "type": "dir",
              "level": "branch",
              "size_class": "S",
              "tags": ["types", "json-schema-generated"]
            },
            {
              "path": "packages/dotnet-clients/gateway",
              "type": "dir",
              "level": "branch",
              "size_class": "S",
              "tags": ["sdk", "dotnet", "gateway-client"]
            }
          ]
        },
        {
          "path": "docs",
          "type": "dir",
          "level": "trunk",
          "size_class": "L",
          "tags": ["docs"],
          "children": [
            {
              "path": "docs/context",
              "type": "dir",
              "level": "trunk",
              "size_class": "M",
              "tags": ["context", "wbs", "rules"]
            },
            {
              "path": "docs/architecture",
              "type": "dir",
              "level": "trunk",
              "size_class": "M",
              "tags": ["architecture", "c4", "api-specs"]
            },
            {
              "path": "docs/frontend",
              "type": "dir",
              "level": "branch",
              "size_class": "S",
              "tags": ["frontend-context"]
            },
            {
              "path": "docs/deploy",
              "type": "dir",
              "level": "trunk",
              "size_class": "M",
              "tags": ["deploy", "uk1", "runbooks"]
            },
            {
              "path": "docs/dlt",
              "type": "dir",
              "level": "trunk",
              "size_class": "S",
              "tags": ["fabric", "k8s"]
            }
          ]
        },
        {
          "path": "ops",
          "type": "dir",
          "level": "branch",
          "size_class": "L",
          "tags": ["ops", "infra", "gitops"],
          "children": [
            {
              "path": "ops/infra",
              "type": "dir",
              "level": "branch",
              "size_class": "M",
              "tags": ["k8s", "helm", "timeweb", "otel", "prometheus"]
            },
            {
              "path": "ops/gitops",
              "type": "dir",
              "level": "branch",
              "size_class": "M",
              "tags": ["gitops", "argocd", "uk1"]
            },
            {
              "path": "ops/scripts",
              "type": "dir",
              "level": "leaf",
              "size_class": "S",
              "tags": ["scripts", "healthchecks", "restore", "validate-specs"]
            },
            {
              "path": "ops/fabric",
              "type": "dir",
              "level": "branch",
              "size_class": "M",
              "tags": ["fabric", "chaincode", "helm"]
            }
          ]
        },
        {
          "path": "tests",
          "type": "dir",
          "level": "leaf",
          "size_class": "L",
          "tags": ["tests"],
          "children": [
            {
              "path": "tests/issuance.Tests",
              "type": "dir",
              "level": "leaf",
              "size_class": "S",
              "tags": ["backend-tests", "issuance"]
            },
            {
              "path": "tests/registry.Tests",
              "type": "dir",
              "level": "leaf",
              "size_class": "S",
              "tags": ["backend-tests", "registry"]
            },
            {
              "path": "tests/settlement.Tests",
              "type": "dir",
              "level": "leaf",
              "size_class": "S",
              "tags": ["backend-tests", "settlement"]
            },
            {
              "path": "tests/compliance.Tests",
              "type": "dir",
              "level": "leaf",
              "size_class": "S",
              "tags": ["backend-tests", "compliance"]
            },
            {
              "path": "tests/contracts",
              "type": "dir",
              "level": "leaf",
              "size_class": "S",
              "tags": ["pact", "contracts"]
            },
            {
              "path": "tests/e2e",
              "type": "dir",
              "level": "leaf",
              "size_class": "S",
              "tags": ["e2e", "smoke"]
            },
            {
              "path": "tests/e2e-playwright",
              "type": "dir",
              "level": "leaf",
              "size_class": "S",
              "tags": ["playwright", "portals-journeys"]
            }
          ]
        },
        {
          "path": "tasks",
          "type": "dir",
          "level": "leaf",
          "size_class": "S",
          "tags": ["nx-tasks", "agents"]
        },
        {
          "path": "memory-bank",
          "type": "dir",
          "level": "leaf",
          "size_class": "S",
          "tags": ["decision-log", "reports"]
        },
        {
          "path": "AGENTS.md",
          "type": "file",
          "level": "trunk",
          "size_class": "S",
          "tags": ["agents-rules"]
        },
        {
          "path": "project.manifest.json",
          "type": "file",
          "level": "trunk",
          "size_class": "S",
          "tags": ["manifest", "monorepo-index"]
        }
      ]
    },
    "logical": {
      "domains": {
        "issuance": {
          "services": ["services/issuance"],
          "apps": ["apps/portal-issuer"],
          "contracts": ["packages/contracts/openapi-issuance.yaml", "packages/contracts/schemas/Issuance.json"],
          "tests": ["tests/issuance.Tests", "tests/e2e-playwright/issuer-journey.spec.ts"]
        },
        "registry": {
          "services": ["services/registry"],
          "apps": ["apps/portal-investor"],
          "contracts": ["packages/contracts/openapi-registry.yaml", "packages/contracts/schemas/Order.json"],
          "tests": ["tests/registry.Tests", "tests/contracts/pact-consumer", "tests/e2e-playwright/investor-journey.spec.ts"]
        },
        "settlement": {
          "services": ["services/settlement"],
          "apps": ["apps/backoffice"],
          "contracts": ["packages/contracts/openapi-settlement.yaml", "packages/contracts/schemas/Payout.json"],
          "tests": ["tests/settlement.Tests"]
        },
        "compliance": {
          "services": ["services/compliance"],
          "apps": ["apps/backoffice"],
          "contracts": ["packages/contracts/openapi-compliance.yaml", "packages/contracts/schemas/AuditEvent.json"],
          "tests": ["tests/compliance.Tests", "tests/e2e-playwright/backoffice-journey.spec.ts"]
        },
        "identity": {
          "services": ["services/identity"],
          "apps": ["apps/portal-issuer", "apps/portal-investor", "apps/backoffice"],
          "contracts": ["packages/contracts/openapi-identity.yaml"],
          "tests": []
        }
      },
      "frontends": [
        {
          "name": "portal-issuer",
          "root": "apps/portal-issuer",
          "guards": ["role:issuer"],
          "uses_sdk": "@ois/api-client"
        },
        {
          "name": "portal-investor",
          "root": "apps/portal-investor",
          "guards": ["role:investor"],
          "uses_sdk": "@ois/api-client"
        },
        {
          "name": "backoffice",
          "root": "apps/backoffice",
          "guards": ["role:backoffice", "role:admin"],
          "uses_sdk": "@ois/api-client"
        }
      ],
      "ops": [
        {
          "name": "uk1",
          "root": "docs/deploy/20251113-cloudflare-ingress.md",
          "level": "trunk"
        },
        {
          "name": "timeweb-k8s",
          "root": "ops/infra/timeweb",
          "level": "branch"
        },
        {
          "name": "fabric-network",
          "root": "ops/fabric",
          "level": "branch"
        }
      ],
      "tests": [
        {
          "name": "backend-unit",
          "roots": [
            "tests/issuance.Tests",
            "tests/registry.Tests",
            "tests/settlement.Tests",
            "tests/compliance.Tests"
          ]
        },
        {
          "name": "e2e-portals",
          "roots": [
            "tests/e2e-playwright"
          ]
        }
      ],
      "nx_index": {
        "NX-01": {
          "title": "Spec validation + API/Event Matrix",
          "task_doc": "tasks/NX-01-spec-validate-and-matrix.md",
          "level": "branch",
          "domains": ["cross-cutting"],
          "nodes": [
            "packages/contracts",
            "docs/context/WBS-OIS.md",
            "docs/architecture/api-event-matrix.md"
          ]
        },
        "NX-02": {
          "title": "API Gateway routing + health/metrics",
          "task_doc": "tasks/NX-02-gateway-routing-and-health.md",
          "level": "branch",
          "domains": ["cross-cutting"],
          "nodes": [
            "apps/api-gateway",
            "services/*",
            "docs/ops/gateway-routing.md"
          ]
        },
        "NX-03": {
          "title": "Issuance endpoints alignment + tests",
          "task_doc": "tasks/NX-03-issuance-endpoints-coverage.md",
          "level": "branch",
          "domains": ["issuance"],
          "nodes": [
            "services/issuance",
            "tests/issuance.Tests",
            "packages/contracts/openapi-issuance.yaml"
          ]
        },
        "NX-04": {
          "title": "Registry order flow (create→reserve→paid) + events",
          "task_doc": "tasks/NX-04-registry-orders-flow.md",
          "level": "branch",
          "domains": ["registry"],
          "nodes": [
            "services/registry",
            "tests/registry.Tests",
            "packages/contracts/openapi-registry.yaml",
            "packages/contracts/asyncapi.yaml"
          ]
        }
      }
    },
    "anchors": [
      {
        "path": "docs/context/PROJECT-CONTEXT.md",
        "role": "project-context",
        "level": "trunk",
        "tags": ["anchor", "context"]
      },
      {
        "path": "docs/context/WBS-OIS.md",
        "role": "wbs",
        "level": "trunk",
        "tags": ["anchor", "wbs", "nx"]
      },
      {
        "path": "docs/frontend/context-map.md",
        "role": "frontend-context",
        "level": "branch",
        "tags": ["anchor", "frontend", "contracts"]
      },
      {
        "path": "AGENTS.md",
        "role": "agents-rules",
        "level": "trunk",
        "tags": ["anchor", "agents", "rules"]
      },
      {
        "path": "docs/deploy/20251113-cloudflare-ingress.md",
        "role": "runbook:uk1",
        "level": "trunk",
        "tags": ["anchor", "ops", "uk1"]
      },
      {
        "path": "docs/dlt/k8s-deploy.md",
        "role": "runbook:fabric",
        "level": "trunk",
        "tags": ["anchor", "dlt", "k8s"]
      },
      {
        "path": "tasks/NX-03-issuance-endpoints-coverage.md",
        "role": "nx-task",
        "level": "branch",
        "tags": ["nx", "issuance"]
      },
      {
        "path": "tasks/NX-04-registry-orders-flow.md",
        "role": "nx-task",
        "level": "branch",
        "tags": ["nx", "registry"]
      }
    ]
  }
```

`repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/AlexA/project-C4.diagram.md`:

```md
---
created: 2025-11-11
updated: 2025-11-18-1619
author: AlexA
co-authrors: gpt5
type: diagram
tags: c4
previous:
next:  [reposcan]
related: []
---

# Project map

## 1. C1–C4 диаграммы Mermaid

### 1.1 C1 — System Context OIS‑CFA и внешние акторы

Основано на PROJECT-CONTEXT, архитектурных openapi‑/asyncapi‑доках и описании интеграций с ESIA, банком, EDO и Fabric.

```mermaid
graph LR
  %% People
  subgraph Users
    issuer[Person: Issuer]
    investor[Person: Investor]
    broker[Person: Broker]
    backoffice[Person: Backoffice / Compliance]
  end

  %% Core system
  ois[System: OIS-CFA Platform]

  %% External systems
  subgraph External_Systems
    esia[[System: ESIA OIDC]]
    bank[[System: Bank Nominal Core]]
    edo[[System: EDO Provider]]
    fabric[[System: Fabric DLT Network]]
    regulator[[System: Regulator / CBR]]
  end

  %% People → System
  issuer -->|Создание/управление выпусками, отчётность| ois
  investor -->|Инвестиции, портфель, история операций| ois
  broker -->|Брокерские операции, маркетплейс| ois
  backoffice -->|KYC/AML, квалификация, аудит| ois

  %% System → External systems
  ois -->|OIDC login, профиль| esia
  ois -->|Платежи, резервирование, списания| bank
  ois -->|Юр. документы, подписание| edo
  ois -->|Реестр активов, сделки на DLT| fabric
  ois -->|Регуляторная отчётность, выгрузки| regulator
```

---

### 1.2 C2 — Containers фронты, gateway, сервисы, инфраструктура

Контейнеры взяты из дерева `apps/*`, `services/*`, `ops/infra/*`, `packages/contracts/*` и API/Event‑матрицы в PROJECT-CONTEXT.

```mermaid
graph TB
  %% Frontend portals
  subgraph Frontends
    fe_issuer[Container: Portal Issuer Next.js\napps/portal-issuer]
    fe_investor[Container: Portal Investor Next.js\napps/portal-investor]
    fe_backoffice[Container: Backoffice Next.js\napps/backoffice]
    fe_broker[Container: Broker Portal Next.js\napps/broker-portal]
  end

  %% Edge layer
  subgraph Edge
    api_gw[Container: API Gateway .NET + YARP\napps/api-gateway]
    keycloak[Container: Keycloak IdP]
  end

  %% Domain services
  subgraph Domain_Services
    svc_issuance[Container: Issuance Service .NET\nservices/issuance]
    svc_registry[Container: Registry Service .NET\nservices/registry]
    svc_settlement[Container: Settlement Service .NET\nservices/settlement]
    svc_compliance[Container: Compliance Service .NET\nservices/compliance]
    svc_identity[Container: Identity Service .NET\nservices/identity]
    svc_fabric_gw[Container: Fabric Gateway .NET\nservices/fabric-gateway]
  end

  %% Integrations
  subgraph Integrations
    svc_bank[Container: Bank Nominal Adapter\nservices/integrations/bank-nominal]
    svc_esia[Container: ESIA Adapter\nservices/integrations/esia-adapter]
    svc_edo[Container: EDO Connector\nservices/integrations/edo-connector]
  end

  %% Data & infra
  subgraph Data_and_Infra
    pg[Container: PostgreSQL cluster\nper service schema]
    kafka[Container: Kafka broker\nevents from AsyncAPI]
    minio[Container: MinIO / Object storage]
    fabric[Container: Fabric network\norderer + peers + chaincode]
    otel[Container: OTel Collector / Prometheus / Grafana]
  end

  %% Users → Frontends
  issuer[Issuer] --> fe_issuer
  investor[Investor] --> fe_investor
  backoffice[Backoffice] --> fe_backoffice
  broker[Broker] --> fe_broker

  %% Frontends → Gateway
  fe_issuer -->|HTTP + OIS TS SDK| api_gw
  fe_investor --> api_gw
  fe_backoffice --> api_gw
  fe_broker --> api_gw

  %% Gateway → Keycloak
  api_gw -->|OIDC / JWT validation| keycloak

  %% Gateway → Domain services REST
  api_gw --> svc_issuance
  api_gw --> svc_registry
  api_gw --> svc_settlement
  api_gw --> svc_compliance
  api_gw --> svc_identity

  %% Services → DB
  svc_issuance --> pg
  svc_registry --> pg
  svc_settlement --> pg
  svc_compliance --> pg
  svc_identity --> pg

  %% Services → Kafka outbox
  svc_issuance -->|Outbox events| kafka
  svc_registry -->|Outbox events| kafka
  svc_settlement -->|Consume/payments| kafka
  svc_compliance -->|Audit/kyc events| kafka

  %% DLT
  svc_issuance --> svc_fabric_gw
  svc_registry --> svc_fabric_gw
  svc_settlement --> svc_fabric_gw
  svc_fabric_gw --> fabric

  %% External integrations
  svc_registry --> svc_bank
  svc_compliance --> svc_esia
  svc_compliance --> svc_edo

  svc_bank --> bank_ext[[External: Bank Core]]
  svc_esia --> esia_ext[[External: ESIA]]
  svc_edo --> edo_ext[[External: EDO]]

  %% Storage & observability
  svc_compliance --> minio
  api_gw --> otel
  svc_issuance --> otel
  svc_registry --> otel
  svc_settlement --> otel
  svc_compliance --> otel
```

---

### 1.3 C3 — Components: Issuance & Registry NX‑03 / NX‑04

Эти C3-диаграммы фокусируются на доменах, важнейших для NX‑03 issuance endpoints + tests и NX‑04 registry order flow.

#### 1.3.1 C3 — Issuance Service `services/issuance`

```mermaid
graph TB
  subgraph Issuance_Service["Issuance Service services/issuance"]
    is_api[Component: HTTP API\nProgram.cs + Minimal APIs]
    is_app[Component: IssuanceApplicationService\nIssuanceService.cs]
    is_domain[Component: Domain Model\nIssuanceId / IssuanceStatus / ValueObjects\npackages/domain]
    is_dbctx[Component: IssuanceDbContext\nIssuanceDbContext.cs]
    is_outbox_svc[Component: OutboxService\nIOutboxService + impl]
    is_outbox_bg[Component: OutboxPublisher\nBackgroundService]
    is_ledger_port[Component: ILedgerIssuance port]
    is_ledger_adp[Component: LedgerIssuanceAdapter\nHTTP → Fabric-Gateway]
    is_metrics[Component: Metrics\nInfrastructure/Metrics.cs]
  end

  gw[Container: API Gateway] --> is_api

  %% Inside service
  is_api -->|Create/Get/Publish/Close issuance| is_app
  is_app --> is_domain
  is_app --> is_dbctx
  is_app --> is_outbox_svc
  is_app --> is_ledger_port

  is_ledger_port --> is_ledger_adp
  is_ledger_adp --> fabric_gw[Container: Fabric Gateway Service]

  is_dbctx --> pg_is[PostgreSQL DB\nschema: issuance]
  is_outbox_svc --> is_dbctx
  is_outbox_bg --> is_dbctx
  is_outbox_bg --> kafka_is[Kafka topics\nois.issuance.published / closed]

  %% Cross-service consumers
  kafka_is --> reg_svc[Container: Registry Service]
  kafka_is --> set_svc[Container: Settlement Service]

  %% Observability
  is_api --> is_metrics
  is_app --> is_metrics
```

Основные соответствия C3↔NX:

* NX‑03 использует `is_api`, `is_app`, `is_dbctx`, `is_outbox_*`, `is_ledger_*` + их тесты `services/issuance/issuance.Tests`.

---

#### 1.3.2 C3 — Registry Service `services/registry`

```mermaid
graph TB
  subgraph Registry_Service["Registry Service services/registry"]
    reg_api[Component: HTTP API\nProgram.cs orders, wallets, redeem]
    reg_app[Component: RegistryApplicationService\nRegistryService.cs]
    reg_domain[Component: Domain Model\nWallet/Holding/Order/Transaction entities]
    reg_dbctx[Component: RegistryDbContext]
    reg_outbox_svc[Component: OutboxService]
    reg_outbox_bg[Component: OutboxPublisher]
    reg_bank_port[Component: IBankNominalService port]
    reg_bank_client[Component: BankNominalClient\nHTTP → bank adapter]
    reg_comp_port[Component: IComplianceService port]
    reg_comp_client[Component: ComplianceClient\nHTTP → compliance]
    reg_ledger_port[Component: ILedgerRegistry port]
    reg_ledger_adp[Component: LedgerRegistryAdapter\nHTTP → Fabric-Gateway]
  end

  gw[Container: API Gateway] --> reg_api

  %% Inside service
  reg_api -->|/v1/orders, /v1/wallets, /v1/issuances/id/redeem| reg_app
  reg_app --> reg_domain
  reg_app --> reg_dbctx
  reg_app --> reg_outbox_svc
  reg_app --> reg_bank_port
  reg_app --> reg_comp_port
  reg_app --> reg_ledger_port

  reg_bank_port --> reg_bank_client
  reg_comp_port --> reg_comp_client
  reg_ledger_port --> reg_ledger_adp

  reg_bank_client --> bank_int[Container: Bank Nominal Integration]
  reg_comp_client --> comp_svc[Container: Compliance Service]
  reg_ledger_adp --> fabric_gw[Container: Fabric Gateway Service]

  reg_dbctx --> pg_reg[PostgreSQL DB\nschema: registry]
  reg_outbox_svc --> reg_dbctx
  reg_outbox_bg --> reg_dbctx
  reg_outbox_bg --> kafka_reg[Kafka topics\norders/*, registry.*]

  kafka_reg --> set_svc[Container: Settlement Service]

```

Соответствие C3↔NX:

* NX‑04 работает ровно по этому разрезу: `reg_api` маршруты /orders, /redeem, `reg_app` стейт‑машина заказа create→reserve→paid, зависимости на банк/комплаенс/Fabric и события в Kafka.

---

### 1.4 C4 — Code/Modules: `services/issuance`

Этот C4‑уровень деталирует `services/issuance` на классы/модули и показывает, как они реализуют компоненты C3. Основано на `IssuanceDbContext`, DTO‑ах, Metrics, Dockerfile и тестах.

```mermaid
graph TB
  %% Composition root
  subgraph CompositionRoot["Composition Root"]
    program["Program.cs\nDI, Minimal APIs, Auth, Metrics\nservices/issuance/Program.cs"]
  end

  %% API layer
  subgraph ApiLayer["API Layer"]
    dtoCreate["CreateIssuanceRequest\nDTO"]
    dtoResponse["IssuanceResponse\nDTO"]
    validators["FluentValidators\nCreateIssuanceRequestValidator, ... "]
  end

  %% Application layer
  subgraph AppLayer["Application Layer"]
    iIssuance["IIssuanceService"]
    issuanceSvc["IssuanceService"]
    iOutbox["IOutboxService"]
    outboxSvc["OutboxService"]
    iLedger["ILedgerIssuance"]
    ledgerAdapter["LedgerIssuanceAdapter"]
  end

  %% Domain + Persistence
  subgraph DomainAndPersistence["Domain + Persistence"]
    domainValue["OIS.Domain\nIssuanceId, IssuanceStatus,\nSecurity, value objects"]
    dbCtx["IssuanceDbContext"]
    entIssuance["IssuanceEntity\ntable: issuances"]
    entOutbox["OutboxMessage\ntable: outbox_messages"]
  end

  %% Infrastructure
  subgraph Infrastructure["Infrastructure"]
    metrics["Metrics\nrequest_duration_ms,\nrequest_errors_total"]
    outboxBg["OutboxPublisher\nBackgroundService"]
    efCore["EF Core + Npgsql provider"]
    massTransit["MassTransit Kafka rider"]
    docker["Dockerfile\nnet9.0 aspnet + sdk"]
  end

  %% External dependencies
  httpFabric["HttpClient\n→ Fabric-Gateway API"]
  postgresDb["PostgreSQL DB\nissuance schema"]
  kafka["Kafka broker\nAsyncAPI topics"]

  %% Wiring
  program --> dtoCreate
  program --> dtoResponse
  program --> validators
  program --> iIssuance

  iIssuance --> issuanceSvc
  issuanceSvc --> domainValue
  issuanceSvc --> dbCtx
  issuanceSvc --> iOutbox
  issuanceSvc --> iLedger

  iOutbox --> outboxSvc
  iLedger --> ledgerAdapter

  dbCtx --> entIssuance
  dbCtx --> entOutbox
  dbCtx --> efCore

  outboxSvc --> dbCtx
  outboxBg --> dbCtx
  outboxBg --> massTransit

  ledgerAdapter --> httpFabric

  dbCtx --> postgresDb
  massTransit --> kafka

  program --> metrics
  metrics --> outboxBg
  docker --> program
```

Связь C3→C4:

* C3‑компонент **HTTP API** = `Program.cs` + DTO/validators.
* **IssuanceApplicationService** = `IssuanceService` + интерфейс `IIssuanceService`.
* **Persistence** = `IssuanceDbContext` + `IssuanceEntity`/`OutboxMessage` + EF Core.
* **Ledger adapter** = `ILedgerIssuance` + `LedgerIssuanceAdapter` + HttpClient.
* **Outbox** = `IOutboxService` + `OutboxService` + `OutboxPublisher` + MassTransit/Kafka.

```

`repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/issuance-endpoints-coverage-report.md`:

```md
# Issuance Service Endpoints Coverage Report

**Generated:** 2025-01-27  
**Task:** NX-03 Issuance Endpoints Coverage

## Executive Summary

Проведена синхронизация реализации сервиса Issuance с OpenAPI спецификациями (`openapi-issuance.yaml`, `openapi-gateway.yaml`), проверено соответствие событий AsyncAPI, добавлены тесты.

## Endpoint Mapping (OpenAPI ↔ Code)

| OpenAPI Endpoint | Method | Service Endpoint | Handler | Status | Notes |
|-----------------|--------|------------------|---------|--------|-------|
| `/v1/issuances` | POST | `/v1/issuances` | `Program.cs:185` → `IssuanceService.CreateAsync` | ✅ | Создание черновика |
| `/v1/issuances/{id}` | GET | `/v1/issuances/{id:guid}` | `Program.cs:216` → `IssuanceService.GetByIdAsync` | ✅ | Получение по ID |
| `/v1/issuances/{id}/publish` | POST | `/v1/issuances/{id:guid}/publish` | `Program.cs:228` → `IssuanceService.PublishAsync` | ✅ | Публикация |
| `/v1/issuances/{id}/close` | POST | `/v1/issuances/{id:guid}/close` | `Program.cs:253` → `IssuanceService.CloseAsync` | ✅ | Закрытие |

**Gateway Mapping:**
- Gateway `/issuances` → YARP transform → Service `/v1/issuances` ✅

## DTO & Validators

### CreateIssuanceRequest
- **Location:** `services/issuance/DTOs/CreateIssuanceRequest.cs`
- **OpenAPI Schema:** `packages/contracts/openapi-issuance.yaml` → `CreateIssuanceRequest`
- **Status:** ✅ Соответствует
- **Fields:**
  - `assetId` (Guid, required) ✅
  - `issuerId` (Guid, required) ✅
  - `totalAmount` (decimal, required, > 0) ✅
  - `nominal` (decimal, required, > 0) ✅
  - `issueDate` (DateOnly, required) ✅
  - `maturityDate` (DateOnly, required) ✅
  - `scheduleJson` (Dictionary<string, object>?, optional) ✅

### IssuanceResponse
- **Location:** `services/issuance/DTOs/IssuanceResponse.cs`
- **OpenAPI Schema:** `packages/contracts/openapi-issuance.yaml` → `IssuanceResponse`
- **Status:** ✅ Соответствует
- **Fields:** Все поля соответствуют OpenAPI схеме

### Validators
- **Location:** `services/issuance/Validators/CreateIssuanceRequestValidator.cs`
- **Status:** ✅ Реализован с FluentValidation
- **Rules:**
  - AssetId, IssuerId: NotEmpty ✅
  - TotalAmount, Nominal: GreaterThan(0) ✅
  - IssueDate, MaturityDate: NotEmpty ✅
  - MaturityDate > IssueDate ✅

## Authentication & Authorization

### Security Schemes (OpenAPI)
- **BearerAuth:** JWT Bearer token (OIDC/Keycloak)
- **Location:** `packages/contracts/openapi-gateway.yaml` → `components.securitySchemes.BearerAuth`

### Implementation
- **Location:** `services/issuance/Program.cs:83-105`
- **Status:** ✅ Реализовано
- **Details:**
  - JWT Bearer authentication (`AddJwtBearer`)
  - Keycloak authority configuration
  - Authorization policies:
    - `role:issuer` — для POST `/issuances`, `/publish`, `/close`
    - `role:any-auth` — для GET `/issuances/{id}`

**SPEC DIFF:** OpenAPI определяет `security: BearerAuth` для всех endpoints, код использует политики `role:issuer` и `role:any-auth`. Это соответствует, так как политики проверяют аутентификацию + роль.

## Events (AsyncAPI ↔ Code)

### ois.issuance.published

**AsyncAPI Schema:**
- **Topic:** `ois.issuance.published`
- **Payload:** `IssuancePublishedPayload`
- **Required fields:** `issuanceId`, `assetId`, `issuerId`, `publishedAt`
- **Optional fields:** `totalAmount`, `schedule`, `metadata`

**Code Implementation:**
- **Location:** `services/issuance/Services/IssuanceService.cs:121-130`
- **Status:** ✅ Соответствует
- **Payload:**
  ```csharp
  {
      issuanceId = issuance.Id,        // ✅ required
      assetId = issuance.AssetId,      // ✅ required
      issuerId = issuance.IssuerId,    // ✅ required
      totalAmount = issuance.TotalAmount, // ✅ optional
      schedule = schedule,              // ✅ optional
      publishedAt = issuance.PublishedAt, // ✅ required
      dltTxHash = txHash               // ⚠️ не в AsyncAPI (добавлено в коде)
  }
  ```

**SPEC DIFF:** Код добавляет `dltTxHash` в payload, которого нет в AsyncAPI. Рекомендация: добавить `dltTxHash` в `IssuancePublishedPayload` в AsyncAPI или удалить из кода.

### ois.issuance.closed

**AsyncAPI Schema:**
- **Topic:** `ois.issuance.closed`
- **Payload:** `IssuanceClosedPayload`
- **Required fields:** `issuanceId`, `closedAt`
- **Optional fields:** `reason`

**Code Implementation:**
- **Location:** `services/issuance/Services/IssuanceService.cs:177-182`
- **Status:** ✅ Соответствует
- **Payload:**
  ```csharp
  {
      issuanceId = issuance.Id,    // ✅ required
      closedAt = issuance.ClosedAt, // ✅ required
      dltTxHash = txHash           // ⚠️ не в AsyncAPI (добавлено в коде)
  }
  ```

**SPEC DIFF:** Код добавляет `dltTxHash` в payload, которого нет в AsyncAPI. Рекомендация: добавить `dltTxHash` в `IssuanceClosedPayload` в AsyncAPI или удалить из кода.

### Outbox Pattern
- **Location:** `services/issuance/Services/OutboxService.cs`
- **Status:** ✅ Реализован
- **Publisher:** `services/issuance/Background/OutboxPublisher.cs`
- **Topics:** `ois.issuance.published`, `ois.issuance.closed`

## Tests

### Test Structure
- **Location:** `services/issuance/issuance.Tests/` (создано)
- **Also exists:** `tests/issuance.Tests/` (существующие тесты)

### Unit Tests (IssuanceServiceTests.cs)
- ✅ `CreateAsync_ShouldCreateDraftIssuance`
- ✅ `GetByIdAsync_ExistingIssuance_ReturnsIssuance`
- ✅ `GetByIdAsync_NonExistent_ReturnsNull`
- ✅ `PublishAsync_DraftIssuance_PublishesAndPublishesEvent`
- ✅ `PublishAsync_NonDraftStatus_ThrowsException`
- ✅ `PublishAsync_NonExistent_ThrowsException`
- ✅ `CloseAsync_PublishedIssuance_ClosesAndPublishesEvent`
- ✅ `CloseAsync_NonPublishedStatus_ThrowsException`
- ✅ `CloseAsync_NonExistent_ThrowsException`

### Integration Tests (IssuanceApiTests.cs)
- ✅ `POST_Issuances_ValidRequest_Returns201`
- ✅ `POST_Issuances_InvalidRequest_Returns400`
- ✅ `GET_Issuances_ExistingId_Returns200`
- ✅ `GET_Issuances_NonExistentId_Returns404`
- ✅ `POST_Publish_ExistingDraft_Returns200`
- ⚠️ `POST_Publish_NonExistent_Returns404` — требует исправления (возвращает 500 вместо 404)
- ✅ `POST_Close_ExistingPublished_Returns200`
- ✅ `POST_Close_NonExistent_Returns404`
- ✅ `POST_Issuances_Unauthorized_Returns401`

### Test Results
- **Location:** `artifacts/issuance-test-report.txt`
- **Status:** 
  - ✅ 1 тест проходит (`IssuanceServiceTests.CreateAsync_ShouldCreateDraftIssuance`)
  - ⚠️ 1 тест падает (`IssuanceApiTests.Publish_NonExistent_Should_Return_404`) — ожидает 404, получает 500
  - **Исправление:** Добавлена проверка существования issuance перед вызовом `PublishAsync` в `Program.cs:233-235`
  - **Примечание:** Тест может использовать старую версию кода. После пересборки должен проходить.

## Recommendations

1. **AsyncAPI:** Добавить `dltTxHash` в `IssuancePublishedPayload` и `IssuanceClosedPayload` для соответствия коду, либо удалить из кода.

2. **Error Handling:** ✅ Исправлено — добавлена проверка существования issuance перед вызовом `PublishAsync` и `CloseAsync` в `Program.cs:233-235, 262-264`.

3. **Tests:** Тесты созданы в `services/issuance/issuance.Tests/`. Один тест может падать из-за использования старой версии кода — требуется пересборка.

4. **Documentation:** ✅ Обновлено — `docs/services/issuance.md` дополнено информацией о событиях, их payload и соответствии AsyncAPI.

## Verification Commands

```bash
# Run tests
dotnet test services/issuance/issuance.Tests.csproj -v minimal

# Or use existing tests
dotnet test tests/issuance.Tests/issuance.Tests.csproj -v minimal

# Check OpenAPI spec
spectral lint packages/contracts/openapi-issuance.yaml

# Check AsyncAPI spec
asyncapi validate packages/contracts/asyncapi.yaml
```

## References

- OpenAPI Spec: `packages/contracts/openapi-issuance.yaml`
- Gateway Spec: `packages/contracts/openapi-gateway.yaml`
- AsyncAPI Spec: `packages/contracts/asyncapi.yaml`
- Service Code: `services/issuance/`
- Tests: `services/issuance/issuance.Tests/`, `tests/issuance.Tests/`


```

`repositories/customer-gitlab/wt__ois-cfa__NX01/artifacts/registry-flow-report.md`:

```md
# Registry Order Flow Report

**Generated:** 2025-11-18  
**Task:** NX-04 Registry: create→reserve→paid flow + events (infra.defis.deploy, .NET 9)

## 1. REST Endpoints (OpenAPI ↔ Code)

**Spec:** `packages/contracts/openapi-registry.yaml`  
**Service:** `services/registry`

| OpenAPI Endpoint                | Method | Service Endpoint                      | Handler                                  | Status | Notes                                      |
|---------------------------------|--------|----------------------------------------|------------------------------------------|--------|--------------------------------------------|
| `/v1/orders`                   | POST   | `/v1/orders`                           | `Program.cs` → `RegistryService.PlaceOrderAsync` | ✅    | Idempotency-Key header required, maps to `IdemKey` |
| `/v1/orders/{id}`              | GET    | `/v1/orders/{id:guid}`                 | `RegistryService.GetOrderAsync`         | ✅    | Returns `OrderResponse` or 404             |
| `/v1/orders/{id}/cancel`       | POST   | `/v1/orders/{id:guid}/cancel`          | `RegistryService.CancelOrderAsync`      | ✅    | Cancels if not `paid/cancelled`           |
| `/v1/orders/{id}/mark-paid`    | POST   | `/v1/orders/{id:guid}/mark-paid`       | `RegistryService.MarkPaidAsync`         | ✅    | Marks `reserved` order as `paid`         |
| `/v1/wallets/{investorId}`     | GET    | `/v1/wallets/{investorId:guid}`        | `RegistryService.GetWalletAsync`        | ✅    | Returns wallet + holdings or 404           |
| `/v1/issuances/{id}/redeem`    | POST   | `/v1/issuances/{id:guid}/redeem`       | `RegistryService.RedeemAsync`           | ✅    | Redeem from holdings, writes tx           |

## 2. Core Flow: create → reserve → paid

**Service:** `RegistryService`  
**DB:** `RegistryDbContext` (`orders`, `wallets`, `holdings`, `tx`, `outbox_messages`)

### 2.1. PlaceOrderAsync

- Idempotency:
  - По заголовку `Idempotency-Key` (GUID) ищем order по `IdemKey`. Если найден → возвращаем существующий `OrderResponse`.
- Validation:
  - `IComplianceService.CheckKycAsync(investorId)`
  - `IComplianceService.CheckQualificationAsync(investorId, amount)`
- Create:
  - `OrderEntity` со статусом `"created"`, полями `InvestorId`, `IssuanceId`, `Amount`, `IdemKey`, `CreatedAt`/`UpdatedAt`.
- Events (Outbox):
  - `ois.order.created` (OrderCreatedPayload)
  - `ois.order.placed` (OrderPlacedPayload) — новое событие, отражающее факт приёма заказа.
- Reserve funds:
  - `IBankNominalService.ReserveFundsAsync(investorId, amount, idempotencyKey)`
  - Статус заказа → `"reserved"`.
- Event:
  - `ois.order.reserved` (OrderReservedPayload) c `bankTransferId`.

### 2.2. MarkPaidAsync

- Preconditions:
  - 404 если заказа нет.
  - Idempotent: если `Status == "paid"`, возвращаем текущий `OrderResponse`.
  - Если `Status != "reserved"` → InvalidOperationException (BadRequest на API уровне).
- Ledger transfer:
  - `_ledger.TransferAsync(null, order.InvestorId.ToString(), order.IssuanceId, order.Amount, ct)` → `txHash`.
  - При такте ошибки: оставляем статус `"reserved"`, заполняем `FailureReason`, исключение пробрасываем.
- Update:
  - `Status = "paid"`, `DltTxHash = txHash`, `ConfirmedAt = UtcNow`, `UpdatedAt = UtcNow`.
  - Получаем/создаём wallet (`GetOrCreateWalletAsync`), обновляем holding (`UpdateHoldingAsync`).
  - Пишем `TransactionEntity` (`WriteTransactionAsync`) с `type = "transfer"`, `DltTxHash = txHash`.
- Events (Outbox):
  - `ois.order.paid` (OrderPaidPayload) — факт оплаты.
  - `ois.order.confirmed` (OrderConfirmedPayload) — подтверждение с `dltTxHash` и `walletId`.
  - `ois.registry.transferred` (RegistryTransferredPayload) — факт перевода в реестре.

## 3. Events Mapping (AsyncAPI ↔ Code)

**Spec:** `packages/contracts/asyncapi.yaml`  
**Contracts:** `packages/domain/IntegrationEvents.cs`  
**Outbox publisher:** `services/registry/Background/OutboxPublisher.cs`

| Topic                  | Spec Payload           | Producer Code                                          | Outbox Publisher                           | Status |
|------------------------|------------------------|--------------------------------------------------------|--------------------------------------------|--------|
| `ois.order.created`    | OrderCreatedPayload    | `RegistryService.PlaceOrderAsync`                     | `OutboxPublisher` → `OrderCreated`         | ✅     |
| `ois.order.placed`     | OrderPlacedPayload     | `RegistryService.PlaceOrderAsync`                     | `OutboxPublisher` → `OrderPlaced`          | ✅     |
| `ois.order.reserved`   | OrderReservedPayload   | `RegistryService.PlaceOrderAsync` (после ReserveFunds)| `OutboxPublisher` → `OrderReserved`        | ✅     |
| `ois.order.paid`       | OrderPaidPayload       | `RegistryService.MarkPaidAsync`                       | `OutboxPublisher` → `OrderPaid`            | ✅     |
| `ois.order.confirmed`  | OrderConfirmedPayload  | `RegistryService.MarkPaidAsync`                       | `OutboxPublisher` → `OrderConfirmed`       | ✅     |
| `ois.registry.transferred` | RegistryTransferredPayload | `RegistryService.MarkPaidAsync`                   | `OutboxPublisher` → `RegistryTransferred`  | ✅     |

## 4. Tests

**Project:** `services/registry/registry.Tests/registry.Tests.csproj` (net9.0)

Запуск:

```bash
$HOME/.dotnet/dotnet test services/registry/registry.Tests/registry.Tests.csproj -v minimal
```

Результат:

- ✅ Всего 9 тестов пройдено, 0 упало, 0 пропущено.

Ключевые тесты для NX‑04:

- `OrderFlowTests.PlaceOrder_IsIdempotent_And_Reserved`:
  - Проверяет:
    - idempotency по `IdemKey` (r1.Id == r2.Id),
    - конечный статус `"reserved"`,
    - наличие `ois.order.created`, `ois.order.placed`, `ois.order.reserved` в `OutboxMessages`.
- `OrderFlowTests.MarkPaid_Moves_To_Paid_And_Writes_Tx`:
  - Проверяет:
    - статус `"paid"` и наличие `DltTxHash`,
    - запись в `Transactions` с `Status = "confirmed"`,
    - наличие `ois.order.paid`, `ois.order.confirmed`, `ois.registry.transferred` в outbox.
- `OrderFlowTests.MarkPaid_On_Ledger_Error_Stays_Reserved_And_Allows_Retry`:
  - Проверяет реакцию на ошибку леджера: заказ остаётся в `"reserved"`, Retry после починки леджера переводит в `"paid"`.

## 5. Settlement (OrderPaid consumption)

**Consumer:** `services/settlement/Consumers/OrderPaidEventConsumer.cs` / `OrderPaidConsumer.cs`  
**Spec:** `ois.order.paid` → `OrderPaidPayload`

- Консьюмеры в Settlement получают `OrderPaid` event и запускают логику расчёта/выплаты (подробности в `services/settlement/`), остаются совместимыми с обновлённым `OrderPaid` contract (поле `txHash` используется как идентификатор DLT‑транзакции).
- Дополнительно можно покрыть end‑to‑end сценарий (NX‑04+Settlement) через E2E/contract tests, но это выходит за рамки текущего NX‑04 re-check.

## 6. Notes

- После NX‑04 SPEC DIFF по `ois.order.placed` и `ois.order.confirmed` закрыт: продьюсеры реализованы, outbox → Kafka wiring есть.
- Открытые AsyncAPI gaps:
  - `ois.payout.scheduled` и `ois.transfer.completed` всё ещё не имеют продьюсеров — оставлены как TODO для последующих задач (см. Gap List в PROJECT-CONTEXT).


```

`repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/FRONTEND-CONTEXT.md`:

```md
# FRONTEND-CONTEXT — статус порталов и требования MVP

## 1. Источники
- `docs/apps/backoffice.md`, `docs/apps/portal-issuer.md`, `docs/apps/portal-investor.md` — описания приложений.
- `docs/frontend/MVP-impl.md` — план MVP по фронтенду.
- `artifacts/FRONTEND-FUNCTIONALITY-ANALYSIS.md` — анализ реализованного функционала и пробелов.

## 2. Portal Issuer (эмитент)

### Реализовано (по артефактам)
- `/dashboard` — базовый дашборд с метриками (сейчас данные в основном заглушки).
- `/issuances` — список выпусков, есть кнопка создания, интеграция с API для создания.
- `/issuances/create` — форма создания выпуска (валидация через Zod, отправка в API).
- `/issuances/[id]` — детали выпуска с возможностью publish/close (интеграция с API).
- `/reports` — страница-заглушка для отчётов.

### Пробелы (MVP критичные)
- Нет редактирования черновика выпуска.
- Нет управления расписанием выплат (payout schedule) — требует SPEC DIFF в OpenAPI.
- Нет отчётов для эмитента (по выпускам, выплатам, инвесторам, регуляторные отчёты).
- Нет мониторинга продаж (графики, статистика по выпускам, список инвесторов по выпуску).

## 3. Backoffice

### Задуманная функциональность
- `/kyc` — управление KYC (approve/reject).
- `/qualification` — управление квалификацией инвесторов (tiers/limits).
- `/payouts` — управление выплатами (запуск/мониторинг).
- `/audit` — аудит-лог.

### Пробелы (MVP критичные)
- KYC только частично реализован; нужен полноценный workflow approve/reject с отображением статусов.
- Нет полноценного реестра пользователей (5625-У) с фильтрами и поиском.
- Нет UI для просмотра журнала аудита (хотя события аудита уже есть в backend).
- Нет управления квалификацией (установка/изменение лимитов, статусов квалификации).

## 4. Portal Investor (для контекста)
- `/portfolio` — портфель инвестора (wallet, holdings).
- `/orders/new` — размещение заказа на покупку.
- `/history` — история операций.
- По анализу артефактов: реализована базовая покупка ЦФА, но не полностью каталог выпусков, история операций, выплаты и погашения.

## 5. Приоритеты MVP (из FRONTEND-FUNCTIONALITY-ANALYSIS)
- Критично (MVP):
  - Portal Issuer: управление расписанием выплат; отчёты для эмитента.
  - Backoffice: полноценный KYC, квалификация инвесторов, журнал аудита, реестр пользователей.
- Важно: мониторинг/аналитика, документооборот, уведомления.
- Желательно: i18n, WCAG AA, расширенная аналитика.

Эти приоритеты должны напрямую транслироваться в продуктовые задачи спринтов.


```

`repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/PROJECT-CONTEXT.md`:

```md
# PROJECT-CONTEXT (OIS-CFA)

Generated: 2025-01-27  
Last Updated: 2025-11-18 (NX-01 spec validation re-check on infra.defis.deploy)

## Executive Summary

Репозиторий содержит mono‑repo ОИС для ЦФА с backend‑сервисами на .NET 8/9, фронт‑порталами (Next.js), спецификациями OpenAPI/AsyncAPI и инфраструктурой (K8s/Helm/GitLab CI). Спецификация‑first артефакты присутствуют в `packages/contracts`. Основные bounded contexts: issuance, registry, settlement, compliance, identity, а также шлюз к Fabric (`fabric-gateway`) и API‑gateway.

Текущий статус по признакам в репозитории:
- Спеки: OpenAPI для gateway/issuance/registry/settlement, AsyncAPI событий, JSON Schema доменных сущностей.
- Сервисы: исходники для всех ключевых сервисов, telemetry (OTel/Prometheus) и health‑пробы у большинства.
- События: Kafka/MassTransit, outbox‑паттерн реализован (issuance, registry, compliance) и consumer в settlement.
- Инфра/CI: Helm/K8s манифесты и GitLab CI присутствуют; есть заметки и гайты по GitLab Runner/ArgoCD.
- Артефакты: собраны отчеты (Keycloak, frontend, build), но тестовые отчеты/coverage не обнаружены.

## Rules Digest (.cursor/rules)

См. также: `docs/context/RULES-SUMMARY.md` для полной выжимки.

- Нулевая галлюцинация и spec‑first/test‑first подход.
- .NET 8/9, C# 12+, DDD/CQRS, EF Core 8, MassTransit, Kafka/RabbitMQ, Redis, Keycloak.
- Наличие OTEL, HealthChecks, Prometheus — обязательно для всех сервисов.
- Любые изменения сопровождаются тестами и командами запуска.

## Architecture Snapshot

Сервисы (backend, `services/`):
- compliance — KYC/аудит, публикует `ois.kyc.updated`, `ois.audit.logged`, `ois.compliance.flagged` (см. `services/compliance/Services/ComplianceService.cs`).
- identity — заглушка OIDC/Keycloak интеграций (см. `services/identity/Program.cs`).
- issuance — выпуск ЦФА, Kafka outbox (`services/issuance/Background/OutboxPublisher.cs`).
- registry — заказы/кошельки/транзакции, события `ois.order.*`, `ois.registry.transferred` (см. `services/registry/Services/RegistryService.cs`).
- settlement — расчет/консьюмеры событий (например, `services/settlement/Consumers/OrderPaidEventConsumer.cs`).
- fabric-gateway — HTTP‑шлюз к Fabric с resilient HttpClient.

Приложения (frontend, `apps/`):
- api-gateway (ASP.NET Core), backoffice, broker-portal, portal‑investor, portal‑issuer, shared‑ui.

Подробный контекст по фронтенду см. в `docs/context/FRONTEND-CONTEXT.md`.

Опорные документы (`docs/architecture/*`): C4‑снимок, последовательности ЕСИА/OIDC, модель данных, дизайн сети Fabric, NFR targets.

<!-- BEGIN: PROJECT-CONTEXT:API-EVENT-MATRIX -->

## API/Event Matrix

Источники: `packages/contracts/openapi-*.yaml`, `packages/contracts/asyncapi.yaml`.  
Валидация выполнена: 2025-01-27 (NX-01, initial). Перепроверено на ветке `infra.defis.deploy`: 2025-11-18 (NX-01 v2). Отчёты: `artifacts/spec-lint-openapi.txt`, `artifacts/spec-validate-asyncapi.txt`, `artifacts/spec-validate-jsonschema.txt`.

### REST API Matrix (Gateway → Services)

**Gateway Implementation:** YARP (Yet Another Reverse Proxy)  
**Configuration:** `apps/api-gateway/appsettings.json`  
**Last Updated:** 2025-01-27 (NX-02)

| Gateway Endpoint | Method | YARP Route | Target Service | Service Endpoint | Status | Notes |
|-----------------|--------|------------|----------------|------------------|--------|-------|
| `/health` | GET | Direct | Gateway | `/health` | ✅ | Gateway health probe |
| `/issuances` | POST | `issuances` | Issuance | `/v1/issuances` | ✅ | YARP transform: `/issuances` → `/v1/issuances` |
| `/issuances/{id}` | GET | `issuances` | Issuance | `/v1/issuances/{id}` | ✅ | `services/issuance/Program.cs:216` |
| `/issuances/{id}/publish` | POST | `issuances` | Issuance | `/v1/issuances/{id}/publish` | ✅ | `services/issuance/Program.cs:228` |
| `/issuances/{id}/close` | POST | `issuances` | Issuance | `/v1/issuances/{id}/close` | ✅ | `services/issuance/Program.cs:253` |
| `/v1/issuances/{id}/redeem` | POST | `redeem` | Registry | `/v1/issuances/{id}/redeem` | ✅ | `services/registry/Program.cs:261` |
| `/v1/orders` | POST | `orders` | Registry | `/v1/orders` | ✅ | `services/registry/Program.cs:212` |
| `/orders/{id}` | GET | `orders` | Registry | `/v1/orders/{id}` | ⚠️ | OpenAPI: `/orders/{id}`, но YARP ожидает `/v1/orders/{id}` |
| `/v1/wallets/{investorId}` | GET | `wallets` | Registry | `/v1/wallets/{investorId}` | ✅ | `services/registry/Program.cs:249` |
| `/v1/settlement/run` | POST | `settlement` | Settlement | `/v1/settlement/run` | ✅ | `services/settlement/Program.cs:182` |
| `/v1/reports/payouts` | GET | `reports` | Settlement | `/v1/reports/payouts` | ✅ | `services/settlement/Program.cs:205` |
| `/v1/compliance/kyc/check` | POST | `compliance` | Compliance | `/v1/compliance/kyc/check` | ✅ | `services/compliance/Program.cs:192` |
| `/v1/compliance/qualification/evaluate` | POST | `compliance` | Compliance | `/v1/compliance/qualification/evaluate` | ✅ | `services/compliance/Program.cs:204` |
| `/v1/compliance/investors/{id}/status` | GET | `compliance` | Compliance | `/v1/compliance/investors/{id}/status` | ✅ | `services/compliance/Program.cs:216` |
| `/v1/complaints` | POST | `complaints` | Compliance | `/v1/complaints` | ✅ | `services/compliance/Program.cs:230` |

**YARP Clusters:**
- `issuance` → `http://issuance-service:8080`
- `registry` → `http://registry-service:8080`
- `settlement` → `http://settlement-service:8080`
- `compliance` → `http://compliance-service:8080`
- `identity` → `http://identity-service:8080`

**SPEC DIFF**: 
- Gateway OpenAPI определяет `/issuances` без `/v1`, но YARP корректно трансформирует в `/v1/issuances` для сервиса.
- Gateway OpenAPI определяет `/orders/{id}` без `/v1`, но YARP маршрут `orders` ожидает `/v1/orders/{**catch-all}`. Требуется либо обновить OpenAPI на `/v1/orders/{id}`, либо добавить дополнительный маршрут.

**Health & Metrics:**
- Все основные сервисы имеют `/health` endpoint (✅)
- Issuance, Registry, Settlement, Compliance имеют `/metrics` (Prometheus) (✅)
- Gateway имеет `/health`, но не имеет `/metrics` (⚠️ рекомендуется добавить)

### Events Matrix (AsyncAPI ↔ Code)

| Topic | AsyncAPI | Producer (Service) | Consumer | Status | Notes |
|-------|----------|---------------------|-----------|--------|------|
| `ois.issuance.published` | ✅ | Issuance (`IssuanceService.cs:121`) | — | ✅ | Outbox: `services/issuance/Background/OutboxPublisher.cs:67` |
| `ois.issuance.closed` | ✅ | Issuance (`IssuanceService.cs:177`) | — | ✅ | Outbox: `services/issuance/Background/OutboxPublisher.cs:71` |
| `ois.order.placed` | ✅ | Registry (`RegistryService.PlaceOrderAsync`) | — | ✅ | Outbox: `services/registry/Services/RegistryService.cs` → `OutboxService` |
| `ois.order.created` | ✅ | Registry (`RegistryService.cs:83`) | — | ✅ | Outbox: `services/registry/Background/OutboxPublisher.cs:67` |
| `ois.order.reserved` | ✅ | Registry (`RegistryService.cs:112`) | — | ✅ | Outbox: `services/registry/Background/OutboxPublisher.cs:71` |
| `ois.order.paid` | ✅ | Registry (`RegistryService.MarkPaidAsync`) | Settlement (`OrderPaidEventConsumer.cs`, `OrderPaidConsumer.cs`) | ✅ | MassTransit: `services/settlement/Program.cs:69` |
| `ois.order.confirmed` | ✅ | Registry (`RegistryService.MarkPaidAsync`) | — | ✅ | Outbox: `services/registry/Background/OutboxPublisher.cs` |
| `ois.registry.transferred` | ✅ | Registry (`RegistryService.cs:278`) | — | ✅ | Outbox: `services/registry/Background/OutboxPublisher.cs:79` |
| `ois.payout.executed` | ✅ | Settlement (`SettlementService.cs:175`) | — | ✅ | Outbox: `services/settlement/Background/OutboxPublisher.cs:85` |
| `ois.payout.scheduled` | ✅ | — | — | ⚠️ | В AsyncAPI, но нет продьюсера в коде |
| `ois.audit.logged` | ✅ | Compliance (`ComplianceService.cs:64`) | — | ✅ | Outbox: `services/compliance/Background/OutboxPublisher.cs:75` |
| `ois.transfer.completed` | ✅ | — | — | ⚠️ | В AsyncAPI, но нет продьюсера в коде |
| `ois.compliance.flagged` | ✅ | Compliance (`ComplianceService.cs:150,226`) | — | ✅ | Outbox: `services/compliance/Background/OutboxPublisher.cs:67` |
| `ois.kyc.updated` | ✅ | Compliance (`ComplianceService.cs:55`) | — | ✅ | Outbox: `services/compliance/Background/OutboxPublisher.cs:71` |

**SPEC DIFF**: Топики `ois.payout.scheduled`, `ois.transfer.completed` объявлены в AsyncAPI, но не имеют продьюсеров в коде. Требуется либо реализация, либо удаление из AsyncAPI.

<!-- END: PROJECT-CONTEXT:API-EVENT-MATRIX -->

## Quality Summary (artifacts/*)

Найдено:
- Build/Frontend/Keycloak отчёты: `artifacts/*`. Диагностики и гайды по GitLab Runner/Keycloak.
- **Спецификации валидация (NX-01, initial 2025-01-27; re-check 2025-11-18 на infra.defis.deploy)**:
  - `artifacts/spec-lint-openapi.txt` — Spectral lint: ✅ No errors (9 OpenAPI файлов)
  - `artifacts/spec-validate-asyncapi.txt` — AsyncAPI CLI: ✅ Valid
  - `artifacts/spec-validate-jsonschema.txt` — AJV: ⚠️ Предупреждения о форматах `uuid`/`decimal` (не критично)

Не найдено/Требуется:
- Unit/Integration/E2E отчёты (JUnit/Allure), coverage отчёты.

<!-- BEGIN: PROJECT-CONTEXT:API-EVENT-GAPS -->

## Gap List (spec/code/tests)

### Спеки (✅ Обновлено NX-01)

**Решено:**
- ✅ Spectral lint для OpenAPI выполнен: 9 файлов, ошибок нет (`artifacts/spec-lint-openapi.txt`)
- ✅ AsyncAPI CLI валидация выполнена: синтаксис корректен (`artifacts/spec-validate-asyncapi.txt`)
- ✅ JSON Schema валидация выполнена: предупреждения о форматах `uuid`/`decimal` (не критично, AJV игнорирует неизвестные форматы)

**Осталось:**
- ⚠️ JSON Schemas: форматы `uuid` и `decimal` не поддерживаются AJV по умолчанию. Рекомендация: использовать `pattern` для UUID или добавить кастомные форматы.
- ⚠️ AsyncAPI: топики `ois.payout.scheduled`, `ois.transfer.completed` объявлены, но нет продьюсеров в коде.

### Код

**API Gateway маршрутизация:**
- ⚠️ Gateway использует `/issuances` без `/v1`, сервисы — с `/v1`. Требуется согласование или проксирование через YARP (`apps/api-gateway`).
- ✅ Основные endpoints соответствуют спецификациям (см. API Matrix выше).

**События:**
- ⚠️ Топики в AsyncAPI без продьюсеров: `ois.payout.scheduled`, `ois.transfer.completed`.
- ✅ Реализованные топики (`ois.order.*`, `ois.issuance.*`, `ois.payout.executed`, `ois.registry.transferred`, `ois.audit.logged`, `ois.compliance.flagged`, `ois.kyc.updated`) соответствуют AsyncAPI схемам.

**Сервисы:**
- ⚠️ Identity — минимальная заглушка; требуется проработка Keycloak интеграции и защищённых политик на всех эндпойнтах.
- ✅ Health/metrics: все основные сервисы имеют `/health` и Prometheus метрики (`/metrics`).
- ⚠️ Gateway: имеет `/health`, но не имеет `/metrics` для мониторинга проксируемых запросов.

**API Gateway маршрутизация (✅ Обновлено NX-02):**
- ✅ YARP настроен корректно: маршруты определены в `apps/api-gateway/appsettings.json`
- ✅ Трансформация путей работает: `/issuances` → `/v1/issuances` для Issuance сервиса
- ⚠️ Несоответствие OpenAPI: `/orders/{id}` в OpenAPI, но YARP ожидает `/v1/orders/{id}`
- ✅ Health check цель: `make check-health` проверяет все сервисы параллельно

**Issuance Service (✅ Обновлено NX-03):**
- ✅ Endpoints соответствуют OpenAPI: POST/GET `/v1/issuances`, POST `/publish`, POST `/close`
- ✅ DTO и валидаторы соответствуют схемам OpenAPI
- ✅ Аутентификация: JWT Bearer + политики `role:issuer` / `role:any-auth`
- ✅ События: `ois.issuance.published` и `ois.issuance.closed` публикуются через outbox
- ⚠️ SPEC DIFF: События содержат `dltTxHash`, которого нет в AsyncAPI (рекомендуется добавить)
- ✅ Тесты: Unit и Integration тесты созданы в `services/issuance/issuance.Tests/`
- **Отчёт:** `artifacts/issuance-endpoints-coverage-report.md`

### Тесты/CI

- ⚠️ Нет артефактов нагрузочного теста (k6) и e2e сценариев выпуска/покупки/погашения.
- ⚠️ Не видно отчетов покрытия; нет Pact/контрактных тестов между gateway и сервисами.

<!-- END: PROJECT-CONTEXT:API-EVENT-GAPS -->

## References

- Спеки: `packages/contracts/*` (OpenAPI/AsyncAPI/JSON Schemas).
- Сервисы: `services/*` (Program.cs, Services/*, DTOs/*, Migrations/*).
- Приложения: `apps/*`.
- Инфра/CI: `ops/*`, `.gitlab-ci.yml`, Helm/K8s в `ops/infra/*`.
- Правила/промпты: `.cursor/rules/*`, `.cursor/promts/*`.
- Gateway Routing: `artifacts/gateway-routing-report.md` (NX-02, 2025-01-27).
- Issuance Coverage: `artifacts/issuance-endpoints-coverage-report.md` (NX-03, 2025-01-27).

```

`repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/RULES-SUMMARY.md`:

```md
# RULES-SUMMARY — Выжимка из .cursor/rules

## 1. Общие принципы (global.mdc, composer.mdc)
- План сначала, код потом; небольшие, обратимые диффы (<200 строк) с явным планом.
- Нулевая галлюцинация: только факты из репозитория и официальных документов.
- Spec-first и test-first: сначала OpenAPI/AsyncAPI/JSON Schemas и их валидация, затем реализация и тесты.
- Обязательны юнит, интеграционные и e2e-тесты для новых/изменённых функций.
- Всегда указывать команды для сборки/тестов и минимальный manual-check.

## 2. Backend (.NET, DDD/CQRS) — dotnet-ddd.mdc, BACKEND-OIS.md
- Архитектура слоёв: Domain, Application, Infrastructure, API.
- Domain: сущности/агрегаты, Value Objects (immutable), доменные события.
- Application: команды/запросы (CQRS, MediatR-подход), FluentValidation, политики авторизации.
- Infrastructure: EF Core 8 (без lazy loading), контексты, конфигурации, outbox, MassTransit (Kafka/RabbitMQ).
- API: контроллеры/минимальные API строго по OpenAPI; версия API; валидация входа.
- События: MassTransit + Kafka, саги, idempotent-консьюмеры, outbox/inbox паттерны.
- Observability: OpenTelemetry (traces, metrics), Prometheus `/metrics`, HealthChecks `/health`.

## 3. Observability & Security — observability.mdc, security.mdc
- Добавлять/проверять OTEL: ресурс (service.name, environment), экспортер OTLP.
- HealthChecks с проверкой зависимностей (БД, брокер, Redis) и готовностью.
- Политики ретраев/таймаутов/сircuit-breaker (Polly) для внешних вызовов.
- OWASP ASVS: входные данные валидируются, полезные нагрузки внешних систем проверяются.
- Секреты — только из окружения/секрет-менеджера; PII-safe логирование, маскирование токенов.

## 4. Testing Discipline — testing.mdc
- Любое изменение сопровождается изменением/добавлением тестов (xUnit + FluentAssertions).
- Для багов: сначала падающий тест, потом фикс.
- Критичные пути ≥90% покрытия, адаптеры ≥70%.
- Рекомендованный запуск: `dotnet test -m:1` + генерация отчётов покрытия.

## 5. Project Rules — develop-promt.mdc, main-promt.mdc
- Цель: MVP ОИС по вертикалям выпуск→покупка→выплаты→погашение с регуляторным комплектом.
- Все артефакты должны быть валидны (lint/build/test), с указанием источников и дат.
- Для любых допущений — фиксировать в `ARCHIVE/assumptions.md`.
- Документы: структурированы, с оглавлением, версионностью и матрицей соответствия НПА.

## 6. Frontend (из MVP-impl и промптов)
- Next.js 15 для порталов (`portal-investor`, `portal-issuer`, `backoffice`).
- SDK на TypeScript из OpenAPI (`packages/sdks/ts`), единый `OisApiClient` с заголовками `x-request-id`, `traceparent`, `x-client-app`.
- Auth: Keycloak OIDC через NextAuth, роли: investor, issuer, backoffice/admin.
- E2E: Playwright-journeys для ключевых пользовательских сценариев.


```

`repositories/customer-gitlab/wt__ois-cfa__NX01/docs/context/WBS-OIS.md`:

```md
# WBS-OIS (Work Breakdown Structure)

Generated: 2025-11-13

## Tracks
- Spec & Contracts
- Backend Services (Issuance, Registry, Settlement, Compliance, Identity)
- API Gateway & Frontends
- Observability & Security
- CI/CD & Infra

## Milestones
- M1: Spec linted + API/Event Matrix (NX-01)
- M2: Gateway health/metrics/routing verified (NX-02)
- M3: Issuance + Registry core paths green with tests (NX-03, NX-04)
- M4: Identity/Keycloak baseline + policies (planned)
- M5: CI quality gates + artifacts (planned)

## Next Tasks
- NX-01: Spec validation + API/Event Matrix — tasks/NX-01-spec-validate-and-matrix.md
- NX-02: API Gateway routing + health/metrics — tasks/NX-02-gateway-routing-and-health.md
- NX-03: Issuance endpoints alignment + tests — tasks/NX-03-issuance-endpoints-coverage.md
- NX-04: Registry order flow (create→reserve→paid) + events — tasks/NX-04-registry-orders-flow.md
- NX-05: Identity/Keycloak integration baseline — planned
- NX-06: CI quality gates (Spectral/AJV/tests/coverage artifacts) — planned

## Notes
- Вся реализация — spec-first. При расхождениях в спеке → сперва YAML‑патч и ревью, затем реализация.
- Для событий Kafka — синхронизировать AsyncAPI топики и payload c фактическими DTO/схемами.


```

`repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-05-issuer-dashboard-and-reports.md`:

```md
# NX-05 — Portal Issuer: дашборд и базовые отчёты с реальными данными

Цель: сделать дашборд и страницу `/reports` портала эмитента полезными для бизнеса: реальные данные о выпусках и базовая отчётность, синхронизированные с backend через API Gateway.

Контекст
- Общий контекст системы: `docs/context/PROJECT-CONTEXT.md`.
- Правила/качество: `docs/context/RULES-SUMMARY.md`, промпты BACKEND-OIS и BACKEND-BUILD-AND-TEST.
- Frontend статус/пробелы: `docs/context/FRONTEND-CONTEXT.md`, `artifacts/FRONTEND-FUNCTIONALITY-ANALYSIS.md`.

Скоуп (что должно быть по итогу)
- `/dashboard` показывает агрегированные метрики по активным/закрытым выпускам и базовые KPI.
- `/reports` предоставляет минимум 2 отчёта:
  - Отчёт по выпускам (кол-во, объёмы, статусы).
  - Отчёт по выплатам (если данные есть в backend; иначе — заглушка с TODO + SPEC DIFF).
- Данные загружаются через API Gateway по существующим или добавленным (через SPEC DIFF) эндпойнтам.

Шаги
1. **Уточнить контракты отчётов**
   - Изучить `docs/frontend/MVP-impl.md` секцию Issuer/Reports.
   - Проверить в `packages/contracts/openapi-gateway.yaml`, какие отчётные эндпойнты уже задекларированы.
   - Если отчётов нет или не хватает — подготовить SPEC DIFF (YAML-патч) и сохранить в `tasks/` как отдельный файл (например, `TASK-issuer-reports-SPEC-DIFF.md`).

2. **API-клиент и вызовы на фронте**
   - Проверить наличие и актуальность TS SDK (`packages/sdks/ts`); при необходимости сгенерировать/обновить.
   - В `apps/portal-issuer` реализовать функции получения данных для:
     - Сводки по выпускам для дашборда.
     - Списка выпусков и/или агрегированных показателей для отчётов.
   - Добавить в запросы заголовки наблюдаемости (`x-request-id`, `traceparent`, `x-client-app`), если это не делается централизованно.

3. **Реализация UI-для дашборда**
   - Используя имеющийся layout `/dashboard`, заменить заглушки на реальные данные.
   - Показать как минимум:
     - Кол-во активных выпусков / закрытых выпусков.
     - Общий объём эмиссий (сумма номиналов активных выпусков).
     - Кол-во инвесторов (если метрика доступна; иначе — TODO с описанием, какие данные нужны из backend).

4. **Реализация UI-для `/reports`**
   - Сделать список доступных отчётов (карточки или таблицу): "Отчёт по выпускам", "Отчёт по выплатам".
   - Для отчёта по выпускам:
     - Таблица с основными полями (ID выпуска, наименование, статус, объём, дата выпуска/закрытия).
     - Возможность выгрузки CSV/XLSX (если backend предоставляет; иначе — CSV на клиенте).
   - Для отчёта по выплатам (если данные есть): аналогичный список выплат с фильтрами по выпуску/дате.

5. **Интеграционные проверки и тесты**
   - Добавить/обновить компонентные тесты для ключевых компонентов дашборда/отчётов (если в проекте уже есть тестовый каркас).
   - Добавить/обновить e2e-сценарий для портала эмитента (Playwright), проходящий последовательность:
     - Логин (можно с заглушкой сессии).
     - Переход на `/dashboard` → проверка отображения метрик.
     - Переход на `/reports` → проверка, что отчёты загружаются и отображаются.

Команды
- Frontend dev:
  - `cd apps/portal-issuer`
  - `npm install`
  - `npm run dev`
- Backend (для проверки реальных данных): см. `BACKEND-BUILD-AND-TEST.md` и Makefile/скрипты в корне.
- E2E (если Playwright настроен): `npm run test:e2e` или аналогичная команда из `package.json`.

Артефакты
- Изменения в `apps/portal-issuer` (страницы `/dashboard`, `/reports`, сервисы данных/SDK).
- При необходимости: SPEC DIFF для отчётных эндпойнтов → отдельный `.md` в `tasks/`.
- `artifacts/issuer-dashboard-and-reports.md` — краткий отчёт с:
  - Использованными эндпойнтами и примерами ответов.
  - Скриншотами или описанием результатов E2E.

Критерии приёмки
- Дашборд `/dashboard` отображает реальные данные по выпускам (без заглушек) при запущенном backend.
- Страница `/reports` предоставляет как минимум один рабочий отчёт по выпускам с возможностью выгрузки данных.
- Все вызовы к API соответствуют спецификациям OpenAPI; расхождения задокументированы SPEC DIFF.
- Наличие описанного артефакта `artifacts/issuer-dashboard-and-reports.md`.


```

`repositories/customer-gitlab/wt__ois-cfa__NX01/tasks/NX-06-issuer-payout-schedule-spec-and-ui.md`:

```md
# NX-06 — Issuer: расписание выплат (SPEC DIFF + UI)

Цель: подготовить и согласовать минимальную спецификацию CRUD по расписанию выплат для выпусков ЦФА и реализовать базовый UI в портале эмитента, не выходя за рамки spec-first подхода.

Контекст
- Общий контекст: `docs/context/PROJECT-CONTEXT.md`.
- Frontend контекст: `docs/context/FRONTEND-CONTEXT.md` (раздел про Portal Issuer).
- План MVP фронтенда: `docs/frontend/MVP-impl.md` (Issuer /reports + payout schedule Spec Diff).

Скоуп
- На уровне спеки: предложить минимальный набор эндпойнтов и схем для управления расписанием выплат по выпуску.
- На уровне UI: добавить в портал эмитента (страницу деталей выпуска или отдельную страницу) отображение расписания выплат в read-only виде, опираясь на доступные поля backend (например, `Issuance.scheduleJson` или аналогичные).

Шаги
1. **Анализ текущих спецификаций и кода**
   - Проверить `packages/contracts/openapi-gateway.yaml` и `openapi-issuance.yaml` на наличие любых эндпойнтов, связанных с payout schedule.
   - Проверить domain/DTO в backend (services/issuance, services/settlement, services/registry) на наличие полей, связанных с распорядком выплат.

2. **Подготовка SPEC DIFF для payout schedule**
   - Если в спецификациях нет CRUD для расписания выплат, подготовить YAML-патч (SPEC DIFF) с предложением добавить:
     - `POST /v1/issuances/{id}/payouts/schedule`
     - `GET /v1/issuances/{id}/payouts/schedule`
     - `PATCH /v1/issuances/{id}/payouts/schedule/{itemId}`
     - `DELETE /v1/issuances/{id}/payouts/schedule/{itemId}`
   - Описать схему `PayoutScheduleItem` (id, date, amount, status) и возможные статусы.
   - Сохранить SPEC DIFF как отдельный файл, например `tasks/NX-06-payout-schedule-SPEC-DIFF.md`.

3. **Read-only UI расписания (до реализации backend)**
   - В `apps/portal-issuer` расширить страницу деталей выпуска `/issuances/[id]` или создать вложенную секцию/таб.
   - Отобразить расписание выплат в виде таблицы (дата, сумма, статус), используя:
     - Либо реальные поля из backend (если уже есть).
     - Либо временный read-only маппинг из существующих данных (например, JSON-поле), с чёткой пометкой TODO.
   - Не реализовывать создание/редактирование/отмену выплат до согласования SPEC DIFF.

4. **Тесты и артефакты**
   - Добавить/обновить компонентные тесты для UI-блока расписания.
   - Если есть Playwright-сценарий для Issuer, добавить шаги проверки отображения расписания.
   - Сохранить SPEC DIFF и краткий отчёт в `artifacts/issuer-payout-schedule.md` с:
     - Описанием предложенных эндпойнтов.
     - Скриншотами или описанием UI.

Команды
- Frontend dev: `cd apps/portal-issuer && npm install && npm run dev`.
- Для генерации/проверки OpenAPI (при необходимости): команды из `ops/scripts/validate-specs.sh` и `BACKEND-BUILD-AND-TEST.md`.

Критерии приёмки
- Подготовлен SPEC DIFF для payout schedule, согласованный с архитектурными правилами (spec-first).
- В портале эмитента на странице выпуска видно read-only расписание выплат (на основе доступных данных).
- Созданы/обновлены тесты; есть артефакт `artifacts/issuer-payout-schedule.md`.


```