# COMPREHENSIVE STUDY GUIDE: INTERNET OF THINGS (IOT): SOCIETAL, SCIENTIFIC, AND TECHNICAL FOUNDATIONS

**Internet of Things (IoT): Societal, Scientific, and Technical Foundations**

*TEGUIA FRANK | UID: 26MCA20153 | Subject Code: 26CAP-608*

## Abstract
This study guide synthesises Inria White Book No. 05 on the Internet of Things. It traces the transition from ubiquitous computing to a global installed base of roughly 10 billion devices, which crossed the 50% tipping point in 2020. It then examines the societal challenges of privacy, sovereignty and sustainability, and the technical challenges created by severe energy and memory constraints. Finally, it maps the research fields of the cloud-edge-thing continuum and condenses the material into definitions, a revision matrix, a question bank and a last-minute reviser.

**Keywords:** Internet of Things; edge computing; lightweight cryptography; federated learning; digital sovereignty; SUIT; RIOT OS

## 1. Study Notes & Core Concepts

### Topic 1: Introduction and Evolution of the Internet of Things
**Core concept.** The Internet of Things is the embodiment of the next-generation Internet: a bridge between the digital and physical worlds, and between standard Internet technologies and heterogeneous embedded systems. It extends network connectivity from people to everyday objects equipped with sensors and actuators.
- **Cyber-Physical Systems (CPS):** Integrated systems in which computational algorithms monitor and control physical processes through sensor-actuator loops.
- **Edge Computing:** A distributed computing model that places computation and storage close to data sources to reduce latency and core-network traffic.
- **Web of Things (WoT):** An application-layer approach that describes and exposes things using web standards such as URIs, HTTP and JSON-LD.
- IoT devices surpassed non-IoT devices in 2020, moving from 10% of connected devices in 2010 to more than 50%.
- The installed base reached roughly 10 billion IoT units, a growth of about 1,000% over the decade.
- Pervasive computing embeds computation and communication into everyday objects.
- The cloud-edge-thing continuum distributes storage and computation across the network.
**Practical example.** In an Industry 4.0 plant, vibration and temperature sensors attached to heavy machinery stream telemetry to an edge gateway, which predicts wear within hours instead of waiting for a scheduled inspection.

### Topic 2: Societal Challenges of an IoT-Enabled World
**Core concept.** IoT is a double-edged sword: it enables automation, optimisation and new services, while creating risks of surveillance, loss of digital sovereignty, dependence on foreign technology providers and a growing environmental footprint. Legal frameworks, public trust, open standards and education are the main societal counterweights.
- **Federated Learning (FL):** A decentralised machine-learning method in which nodes train a shared model locally and exchange model updates rather than raw data.
- **Digital Sovereignty:** The ability of individuals or states to retain control over their digital infrastructure, data and technology supply chain.
- **Surveillance Capitalism:** An economic model built on harvesting, processing and monetising behavioural data captured by pervasive sensors and trackers.
- Permissionless innovation must be balanced against ethical concerns and public trust.
- Digital sovereignty covers data, infrastructure and the technology supply chain.
- Open standards and open source act as a common public good for IoT.
- Education is needed so that citizens understand the technological foundations of IoT.
**Practical example.** The General Data Protection Regulation (GDPR) gives European consumers legal protection against unauthorised tracking by smart-home devices and illustrates how regulation can balance innovation with privacy.

### Topic 3: Scientific and Technical Challenges of IoT
**Core concept.** Low-end IoT devices operate under severe resource constraints: microscopic energy budgets, limited RAM and flash, slow processors and low-bandwidth wireless links. These constraints invalidate traditional security, networking, database and machine-learning assumptions and require lightweight, energy-aware designs.
- **Lightweight Cryptography:** Cryptographic primitives optimised to run securely within the energy, memory and CPU limits of constrained hardware.
- **Intermittent Computing:** A computing model for battery-less, energy-harvesting nodes that preserves state across frequent power failures using non-volatile memory.
- **Object Security (OSCORE):** End-to-end protection applied to the application-layer payload rather than relying only on the transport channel.
- Energy and memory budgets on low-end nodes are orders of magnitude below those of cloud servers.
- Lightweight cryptography and object security protect constrained devices.
- Federated learning keeps raw data on-device and shares model updates instead.
- Intermittent computing lets battery-less nodes survive frequent power failures.
**Practical example.** An artificial pancreas adjusts insulin delivery from continuous glucose monitoring. A software bug or cyberattack can directly threaten human life, so cyber-safety and cyber-security must be designed together.

### Topic 4: Architecture and Research Fields of the Cloud-Edge-Thing Continuum
**Core concept.** IoT systems are organised as a continuum from tiny things, through edge gateways, to cloud data centres. Research spans communication networks, semantic data representation, distributed systems, cryptology, privacy, safety, human-machine interaction and low-power hardware.
- **Cyber-Physical Systems (CPS):** Integrated systems in which computational algorithms monitor and control physical processes through sensor-actuator loops.
- **Edge Computing:** A distributed computing model that places computation and storage close to data sources to reduce latency and core-network traffic.
- **Web of Things (WoT):** An application-layer approach that describes and exposes things using web standards such as URIs, HTTP and JSON-LD.
- 6LoWPAN, CoAP, LoRaWAN and 5G provide complementary last-hop connectivity options.
- The Web of Things standardises object descriptions with web standards such as URIs and JSON-LD.
- Middleware and DevOps toolchains must manage heterogeneous edge and cloud resources.
- Safety, reliability and certification are first-class concerns in cyber-physical systems.
**Practical example.** A smart marina combines low-power wireless sensors, an edge gateway and a cloud dashboard to monitor slip availability, energy use and water quality without continuously transmitting raw measurements.

## 2. Structured Revision Points
### Key Facts and Statistics
- Between 2010 and 2020 the share of IoT devices among all connected devices rose from 10% to more than 50%, a growth of about 1,000%.
- The global installed base reached roughly 10 billion IoT devices by 2020, so IoT officially passed the tipping point.
- More than 28 billion microcontrollers were shipped in 2018, with an estimated 250 billion in use worldwide by 2020.
- A constrained IoT node may have only about 0.001% of the memory budget of a traditional Internet-connected machine.
- ChaCha20 can deliver roughly a 30% performance improvement over AES on microcontrollers that lack hardware AES acceleration.
- RIOT is a vendor-independent, open-source operating system for resource-constrained microcontrollers that cannot run Linux.
- SUIT defines a signed manifest that lets a device verify the authenticity and integrity of a firmware update before installation.
- Federated learning shares model updates instead of raw data, reducing privacy exposure in distributed IoT analytics.
- The Web of Things uses web standards to make heterogeneous things interoperable across application domains.
- Digital sovereignty requires control over data, infrastructure and the technology supply chain, not only over applications.
- The General Data Protection Regulation (EU 2016/679) provides a legal framework for protecting personal data in connected products.
- Open standards and open-source software reduce vendor lock-in and help devices remain supported over long service lifetimes.

### Sequential Process: Secure IoT Software Update (SUIT)
- Phase 0 - Commission: provision the device with a public key and symmetric master credentials out of band.
- Phase 1 - Build: compile the new firmware into a deployment-ready image.
- Phase 2 - Publish and sign: create a signed manifest containing hashes and publish the package.
- Phase 3 - Fetch: the constrained device polls and downloads the update package.
- Phase 4 - Authenticate and verify: check the signature and SHA-256 hashes before installation.
- Phase 5 - Install or abort: install only on success; otherwise abort and raise a security alert.

### Comparative Framing: Symmetric vs Asymmetric Cryptography
- **Symmetric cryptography (ChaCha20, AES):** one shared secret key; fast, energy-efficient and ideal for bulk payloads, but key distribution is hard.
- **Asymmetric cryptography (ECC, post-quantum schemes):** a public/private key pair enables signatures and key exchange, but costs more CPU, memory and energy.

## 3. Quick Revision Matrix
| Research Field / Domain | Core Definition | Primary IoT Use Cases |
|---|---|---|
| Communication Networks | Protocols and radio technologies that optimise wireless physical links for constrained nodes. | 5G, LoRaWAN, 6LoWPAN, multi-hop mesh and deterministic networking. |
| Data Representation (WoT) | Semantic models and web standards that describe things, their properties and interactions. | Web of Things, JSON-LD, linked data and interoperable thing directories. |
| Distributed Systems | Software layers and toolchains that manage computation across cloud, edge and thing tiers. | IoT middleware, container orchestration at the edge and embedded DevOps. |
| Cryptology for Low-End IoT | Lightweight symmetric and asymmetric primitives designed for tight power, memory and CPU budgets. | ChaCha20, AES-128, elliptic-curve cryptography and post-quantum candidates. |
| Data Processing and Privacy | Techniques that preserve analytical utility while minimising disclosure of raw personal data. | Federated learning, differential privacy and on-device analytics. |
| Safety, Reliability and Certification | Methods for proving that cyber-physical systems fail safely and meet regulatory assurance levels. | Formal verification, fault injection and safety cases for medical or automotive devices. |
| Human-Machine Interaction | Interfaces and interaction models that make ubiquitous sensing understandable and controllable. | Ambient notifications, tangible controls and privacy dashboards. |
| Control with IoT in the Loop | Control theory for feedback loops whose sensing and actuation traverse a network. | Latency-aware controllers for robotics, smart grids and industrial automation. |
| Security for IoT | End-to-end protection of devices, networks and update channels against cyber and physical attacks. | Secure boot, OSCORE object security and SUIT firmware updates. |
| Low-Power Hardware, Programming and Compiling | Processor, memory and compiler techniques that minimise energy per operation. | RISC-V microcontrollers, non-volatile memory and intermittent computing. |
| Global Resource Footprint Optimisation | Life-cycle methods that reduce the energy, material and carbon cost of IoT deployments. | Energy harvesting, battery-less nodes and circular hardware design. |

## 4. Exam-Oriented Question Bank

### Short-Answer / Conceptual Questions
1. Define Cyber-Physical Systems (CPS) and explain why it matters in a constrained IoT system.
   **Answer:** Integrated systems in which computational algorithms monitor and control physical processes through sensor-actuator loops.
2. Define Edge Computing and explain why it matters in a constrained IoT system.
   **Answer:** A distributed computing model that places computation and storage close to data sources to reduce latency and core-network traffic.
3. Define Lightweight Cryptography and explain why it matters in a constrained IoT system.
   **Answer:** Cryptographic primitives optimised to run securely within the energy, memory and CPU limits of constrained hardware.
4. Define Federated Learning (FL) and explain why it matters in a constrained IoT system.
   **Answer:** A decentralised machine-learning method in which nodes train a shared model locally and exchange model updates rather than raw data.
5. Define Digital Sovereignty and explain why it matters in a constrained IoT system.
   **Answer:** The ability of individuals or states to retain control over their digital infrastructure, data and technology supply chain.

### Practical / Scenario-Based Questions
1. A smart-city project deploys battery-powered environmental sensors in a valley with no cellular coverage. Identify the main energy, bandwidth and maintenance constraints and propose an architecture.
   **Answer:** Use low-power wide-area networking or multi-hop mesh, duty-cycle the radio, process data at an edge gateway, and use energy harvesting with intermittent-computing support.
2. An industrial control loop receives sensor packets 200 ms late during network congestion, causing instability. Explain the cause and propose a mitigation.
   **Answer:** The delay violates the control loop's timing budget. Move the controller to the edge, prioritise its traffic, and design the controller to tolerate bounded jitter.
3. A manufacturer discovers a remotely exploitable vulnerability in an insulin pump. Outline a safe remediation lifecycle.
   **Answer:** Provision keys, build and sign a SUIT manifest, distribute the package, verify signature and hashes on-device, install atomically, and abort with an alert if verification fails.

### Multiple-Choice Questions
1. Which open-source operating system is designed for microcontrollers that cannot run Linux?
   - Android Embedded
   - RIOT
   - Windows IoT Core
   - Ubuntu Touch
   **Answer:** B) RIOT
2. Which property makes ChaCha20 attractive on microcontrollers without hardware AES acceleration?
   - It removes the need for keys
   - It is fast in software
   - It increases key length to 1024 bits
   - It needs no memory
   **Answer:** B) It is fast in software
3. What does federated learning keep on the device?
   - Only the final model
   - Raw training data
   - The central server logs
   - The encryption key
   **Answer:** B) Raw training data
4. Which update standard defines a signed manifest for constrained devices?
   - SUIT
   - SMTP
   - X10
   - HTML5
   **Answer:** A) SUIT

## 5. Last-Minute Reviser
- IoT passed the tipping point in 2020: more than half of all connected devices are IoT devices.
- Low-end nodes are constrained by energy first, then memory, CPU and network throughput.
- Use symmetric ciphers for bulk data and asymmetric primitives for signatures and key exchange.
- Federated learning shares model updates, not raw personal data.
- Secure updates require a signed manifest, hash verification and an atomic install/abort decision.
- The cloud-edge-thing continuum trades centralisation for latency, bandwidth and privacy.
- Digital sovereignty concerns infrastructure and standards, not only applications.
- Open standards and open source reduce lock-in and support long device lifetimes.

---
*Generated by the AI-Assisted Multi-Format Content Studio on 31 October 2026.*