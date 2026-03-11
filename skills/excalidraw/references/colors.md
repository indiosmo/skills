# Color Palettes Reference

Color schemes for architecture diagrams across different platforms and component types.

---

## Default Palette (Platform-Agnostic)

Use this palette for general architecture diagrams.

| Component Type | Background | Stroke | Example Use |
|----------------|------------|--------|-------------|
| Frontend/UI | `#a5d8ff` | `#1971c2` | Next.js, React, Vue apps |
| Backend/API | `#d0bfff` | `#7048e8` | API servers, microservices |
| Database | `#b2f2bb` | `#2f9e44` | PostgreSQL, MySQL, MongoDB |
| Storage | `#ffec99` | `#f08c00` | Object storage, file systems |
| AI/ML Services | `#e599f7` | `#9c36b5` | ML models, AI APIs |
| External APIs | `#ffc9c9` | `#e03131` | Third-party services |
| Orchestration | `#ffa8a8` | `#c92a2a` | Workflows, schedulers, hubs |
| Validation | `#ffd8a8` | `#e8590c` | Validators, checkers |
| Network/Security | `#dee2e6` | `#495057` | VPC, IAM, firewalls |
| Classification | `#99e9f2` | `#0c8599` | Routers, classifiers |
| Users/Actors | `#e7f5ff` | `#1971c2` | User ellipses |
| Message Queue | `#fff3bf` | `#fab005` | Kafka, RabbitMQ, SQS |
| Cache | `#ffe8cc` | `#fd7e14` | Redis, Memcached |
| Monitoring | `#d3f9d8` | `#40c057` | Prometheus, Grafana |

---

## AWS Palette

Use when diagramming AWS infrastructure.

| Service Category | Background | Stroke | Examples |
|-----------------|------------|--------|----------|
| Compute | `#ff9900` | `#cc7a00` | EC2, Lambda, ECS, EKS |
| Storage | `#3f8624` | `#2d6119` | S3, EBS, EFS |
| Database | `#3b48cc` | `#2d3899` | RDS, DynamoDB, Aurora |
| Networking | `#8c4fff` | `#6b3dcc` | VPC, Route53, CloudFront |
| Security | `#dd344c` | `#b12a3d` | IAM, KMS, Cognito |
| Analytics | `#8c4fff` | `#6b3dcc` | Kinesis, Athena, EMR |
| ML/AI | `#01a88d` | `#017d69` | SageMaker, Bedrock |
| Messaging | `#ff4f8b` | `#cc3f6f` | SQS, SNS, EventBridge |

---

## Azure Palette

Use when diagramming Azure infrastructure.

| Service Category | Background | Stroke | Examples |
|-----------------|------------|--------|----------|
| Compute | `#0078d4` | `#005a9e` | VMs, Functions, AKS |
| Storage | `#50e6ff` | `#3cb5cc` | Blob Storage, Files |
| Database | `#0078d4` | `#005a9e` | SQL Database, Cosmos DB |
| Networking | `#773adc` | `#5a2ca8` | VNet, DNS, CDN |
| Security | `#ff8c00` | `#cc7000` | AD, Key Vault |
| AI/ML | `#50e6ff` | `#3cb5cc` | Azure ML, Cognitive Services |

---

## GCP Palette

Use when diagramming Google Cloud infrastructure.

| Service Category | Background | Stroke | Examples |
|-----------------|------------|--------|----------|
| Compute | `#4285f4` | `#3367d6` | GCE, Cloud Run, GKE |
| Storage | `#34a853` | `#2d8e47` | Cloud Storage |
| Database | `#ea4335` | `#c53929` | Cloud SQL, Firestore, Spanner |
| Networking | `#fbbc04` | `#d99e04` | VPC, Cloud DNS, Load Balancer |
| AI/ML | `#9334e6` | `#7627b8` | Vertex AI, AutoML |
| Messaging | `#4285f4` | `#3367d6` | Pub/Sub, Cloud Tasks |

---

## Kubernetes Palette

Use when diagramming Kubernetes architecture.

| Component | Background | Stroke | Notes |
|-----------|------------|--------|-------|
| Pod | `#326ce5` | `#2756b8` | K8s blue |
| Service | `#326ce5` | `#2756b8` | |
| Deployment | `#326ce5` | `#2756b8` | |
| ConfigMap/Secret | `#7f8c8d` | `#626d6e` | Gray for config |
| Ingress | `#00d4aa` | `#00a888` | Green for entry points |
| Node | `#303030` | `#1a1a1a` | Dark for infrastructure |
| Namespace | `#f0f0f0` | `#c0c0c0` | Light, use dashed stroke |

---

## Diagram Type Suggestions

| Diagram Type | Recommended Palette | Key Elements |
|--------------|---------------------|--------------|
| Microservices | Default | Services (purple), databases (green), queues (yellow), API gateway (blue) |
| Data Pipeline | Default | Sources (blue), transformers (purple), sinks (green), storage (yellow) |
| Event-Driven | Default | Event bus (coral), producers/consumers (various) |
| Kubernetes | Kubernetes | Namespace boxes, pods, services, ingress |
| AWS Architecture | AWS | Use AWS colors for AWS services |
| Azure Architecture | Azure | Use Azure colors for Azure services |
| GCP Architecture | GCP | Use GCP colors for GCP services |
| Multi-Cloud | Mixed | Use respective cloud colors per service |
| CI/CD Pipeline | Default | Source (blue), build (purple), test (yellow), deploy (green) |
| Network Topology | Default | VPC (gray), subnets (light), instances (blue) |

---

## Color Usage Guidelines

### Contrast

- Ensure stroke color is darker than background
- Text inside shapes should be readable against background
- Default text color: `#1e1e1e`

### Consistency

- Same component type = same color throughout diagram
- Use arrows matching the destination color for flow indication
- Group boundaries should be lighter/more transparent than contents

### Semantic Meaning

- **Blue tones**: Frontend, networking, general compute
- **Purple tones**: Backend, processing, APIs
- **Green tones**: Databases, storage, success states
- **Yellow/Orange tones**: Caching, warnings, validation
- **Red/Coral tones**: External services, orchestration, important elements
- **Gray tones**: Infrastructure, security, configuration

---

## Quick Reference

### Most Common Combinations

```
Frontend:    #a5d8ff / #1971c2
API:         #d0bfff / #7048e8
Database:    #b2f2bb / #2f9e44
Cache:       #ffe8cc / #fd7e14
Queue:       #fff3bf / #fab005
External:    #ffc9c9 / #e03131
User:        #e7f5ff / #1971c2 (ellipse)
```

### Group/Boundary Styles

```json
{
  "backgroundColor": "transparent",
  "strokeColor": "#9c36b5",
  "strokeStyle": "dashed",
  "strokeWidth": 1
}
```
