"""Domain profile for the IoT white-book case study.

The generic pipeline works on any technical document.  For the assessed case
study we add a small, source-grounded domain profile: terminology, a fact bank
and the canonical section names used by the four phase prompts.  Every fact in
this file is taken from the Inria White Book No. 05 (November 2021).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TopicSpec:
    title: str
    query: str
    core: str
    example: str
    pills: tuple[str, ...]


@dataclass(frozen=True)
class FieldSpec:
    name: str
    definition: str
    use_case: str


IOT_TOPICS: tuple[TopicSpec, ...] = (
    TopicSpec(
        title="Introduction and Evolution of the Internet of Things",
        query=(
            "internet of things evolution ubiquitous computing tipping point "
            "connected devices pervasive computing prehistory"
        ),
        core=(
            "The Internet of Things is the embodiment of the next-generation Internet: "
            "a bridge between the digital and physical worlds, and between standard "
            "Internet technologies and heterogeneous embedded systems. It extends "
            "network connectivity from people to everyday objects equipped with "
            "sensors and actuators."
        ),
        example=(
            "In an Industry 4.0 plant, vibration and temperature sensors attached to "
            "heavy machinery stream telemetry to an edge gateway, which predicts wear "
            "within hours instead of waiting for a scheduled inspection."
        ),
        pills=(
            "IoT devices surpassed non-IoT devices in 2020, moving from 10% of connected devices in 2010 to more than 50%.",
            "The installed base reached roughly 10 billion IoT units, a growth of about 1,000% over the decade.",
            "Pervasive computing embeds computation and communication into everyday objects.",
            "The cloud-edge-thing continuum distributes storage and computation across the network.",
        ),
    ),
    TopicSpec(
        title="Societal Challenges of an IoT-Enabled World",
        query=(
            "societal challenges privacy public trust legal framework sovereignty "
            "standardization education climate change resource depletion surveillance"
        ),
        core=(
            "IoT is a double-edged sword: it enables automation, optimisation and new "
            "services, while creating risks of surveillance, loss of digital sovereignty, "
            "dependence on foreign technology providers and a growing environmental "
            "footprint. Legal frameworks, public trust, open standards and education "
            "are the main societal counterweights."
        ),
        example=(
            "The General Data Protection Regulation (GDPR) gives European consumers "
            "legal protection against unauthorised tracking by smart-home devices and "
            "illustrates how regulation can balance innovation with privacy."
        ),
        pills=(
            "Permissionless innovation must be balanced against ethical concerns and public trust.",
            "Digital sovereignty covers data, infrastructure and the technology supply chain.",
            "Open standards and open source act as a common public good for IoT.",
            "Education is needed so that citizens understand the technological foundations of IoT.",
        ),
    ),
    TopicSpec(
        title="Scientific and Technical Challenges of IoT",
        query=(
            "technical challenges resource constraints energy memory low-power security "
            "privacy machine learning last hop networking intermittent computing"
        ),
        core=(
            "Low-end IoT devices operate under severe resource constraints: microscopic "
            "energy budgets, limited RAM and flash, slow processors and low-bandwidth "
            "wireless links. These constraints invalidate traditional security, "
            "networking, database and machine-learning assumptions and require "
            "lightweight, energy-aware designs."
        ),
        example=(
            "An artificial pancreas adjusts insulin delivery from continuous glucose "
            "monitoring. A software bug or cyberattack can directly threaten human "
            "life, so cyber-safety and cyber-security must be designed together."
        ),
        pills=(
            "Energy and memory budgets on low-end nodes are orders of magnitude below those of cloud servers.",
            "Lightweight cryptography and object security protect constrained devices.",
            "Federated learning keeps raw data on-device and shares model updates instead.",
            "Intermittent computing lets battery-less nodes survive frequent power failures.",
        ),
    ),
    TopicSpec(
        title="Architecture and Research Fields of the Cloud-Edge-Thing Continuum",
        query=(
            "communication networks data representation distributed systems cloud edge "
            "thing continuum research fields middleware interoperability"
        ),
        core=(
            "IoT systems are organised as a continuum from tiny things, through edge "
            "gateways, to cloud data centres. Research spans communication networks, "
            "semantic data representation, distributed systems, cryptology, privacy, "
            "safety, human-machine interaction and low-power hardware."
        ),
        example=(
            "A smart marina combines low-power wireless sensors, an edge gateway and a "
            "cloud dashboard to monitor slip availability, energy use and water quality "
            "without continuously transmitting raw measurements."
        ),
        pills=(
            "6LoWPAN, CoAP, LoRaWAN and 5G provide complementary last-hop connectivity options.",
            "The Web of Things standardises object descriptions with web standards such as URIs and JSON-LD.",
            "Middleware and DevOps toolchains must manage heterogeneous edge and cloud resources.",
            "Safety, reliability and certification are first-class concerns in cyber-physical systems.",
        ),
    ),
)

IOT_FIELDS: tuple[FieldSpec, ...] = (
    FieldSpec(
        "Communication Networks",
        "Protocols and radio technologies that optimise wireless physical links for constrained nodes.",
        "5G, LoRaWAN, 6LoWPAN, multi-hop mesh and deterministic networking.",
    ),
    FieldSpec(
        "Data Representation (WoT)",
        "Semantic models and web standards that describe things, their properties and interactions.",
        "Web of Things, JSON-LD, linked data and interoperable thing directories.",
    ),
    FieldSpec(
        "Distributed Systems",
        "Software layers and toolchains that manage computation across cloud, edge and thing tiers.",
        "IoT middleware, container orchestration at the edge and embedded DevOps.",
    ),
    FieldSpec(
        "Cryptology for Low-End IoT",
        "Lightweight symmetric and asymmetric primitives designed for tight power, memory and CPU budgets.",
        "ChaCha20, AES-128, elliptic-curve cryptography and post-quantum candidates.",
    ),
    FieldSpec(
        "Data Processing and Privacy",
        "Techniques that preserve analytical utility while minimising disclosure of raw personal data.",
        "Federated learning, differential privacy and on-device analytics.",
    ),
    FieldSpec(
        "Safety, Reliability and Certification",
        "Methods for proving that cyber-physical systems fail safely and meet regulatory assurance levels.",
        "Formal verification, fault injection and safety cases for medical or automotive devices.",
    ),
    FieldSpec(
        "Human-Machine Interaction",
        "Interfaces and interaction models that make ubiquitous sensing understandable and controllable.",
        "Ambient notifications, tangible controls and privacy dashboards.",
    ),
    FieldSpec(
        "Control with IoT in the Loop",
        "Control theory for feedback loops whose sensing and actuation traverse a network.",
        "Latency-aware controllers for robotics, smart grids and industrial automation.",
    ),
    FieldSpec(
        "Security for IoT",
        "End-to-end protection of devices, networks and update channels against cyber and physical attacks.",
        "Secure boot, OSCORE object security and SUIT firmware updates.",
    ),
    FieldSpec(
        "Low-Power Hardware, Programming and Compiling",
        "Processor, memory and compiler techniques that minimise energy per operation.",
        "RISC-V microcontrollers, non-volatile memory and intermittent computing.",
    ),
    FieldSpec(
        "Global Resource Footprint Optimisation",
        "Life-cycle methods that reduce the energy, material and carbon cost of IoT deployments.",
        "Energy harvesting, battery-less nodes and circular hardware design.",
    ),
)

IOT_GLOSSARY: tuple[tuple[str, str], ...] = (
    ("Cyber-Physical Systems (CPS)",
     "Integrated systems in which computational algorithms monitor and control physical processes through sensor-actuator loops."),
    ("Edge Computing",
     "A distributed computing model that places computation and storage close to data sources to reduce latency and core-network traffic."),
    ("Lightweight Cryptography",
     "Cryptographic primitives optimised to run securely within the energy, memory and CPU limits of constrained hardware."),
    ("Federated Learning (FL)",
     "A decentralised machine-learning method in which nodes train a shared model locally and exchange model updates rather than raw data."),
    ("Digital Sovereignty",
     "The ability of individuals or states to retain control over their digital infrastructure, data and technology supply chain."),
    ("Web of Things (WoT)",
     "An application-layer approach that describes and exposes things using web standards such as URIs, HTTP and JSON-LD."),
    ("Intermittent Computing",
     "A computing model for battery-less, energy-harvesting nodes that preserves state across frequent power failures using non-volatile memory."),
    ("Object Security (OSCORE)",
     "End-to-end protection applied to the application-layer payload rather than relying only on the transport channel."),
    ("SUIT",
     "A standardised manifest format for secure firmware updates on constrained IoT devices."),
    ("Surveillance Capitalism",
     "An economic model built on harvesting, processing and monetising behavioural data captured by pervasive sensors and trackers."),
    ("Smart Dust",
     "Millimetre-scale or smaller motes that can sense, compute and communicate without a conventional circuit board."),
    ("Dual Prediction Minimisation",
     "An energy-saving technique in which node and edge run matching predictors and transmit only when a measurement deviates."),
)

IOT_FACTS: tuple[str, ...] = (
    "Between 2010 and 2020 the share of IoT devices among all connected devices rose from 10% to more than 50%, a growth of about 1,000%.",
    "The global installed base reached roughly 10 billion IoT devices by 2020, so IoT officially passed the tipping point.",
    "More than 28 billion microcontrollers were shipped in 2018, with an estimated 250 billion in use worldwide by 2020.",
    "A constrained IoT node may have only about 0.001% of the memory budget of a traditional Internet-connected machine.",
    "ChaCha20 can deliver roughly a 30% performance improvement over AES on microcontrollers that lack hardware AES acceleration.",
    "RIOT is a vendor-independent, open-source operating system for resource-constrained microcontrollers that cannot run Linux.",
    "SUIT defines a signed manifest that lets a device verify the authenticity and integrity of a firmware update before installation.",
    "Federated learning shares model updates instead of raw data, reducing privacy exposure in distributed IoT analytics.",
    "The Web of Things uses web standards to make heterogeneous things interoperable across application domains.",
    "Digital sovereignty requires control over data, infrastructure and the technology supply chain, not only over applications.",
    "The General Data Protection Regulation (EU 2016/679) provides a legal framework for protecting personal data in connected products.",
    "Open standards and open-source software reduce vendor lock-in and help devices remain supported over long service lifetimes.",
)

IOT_TIMELINE: tuple[tuple[str, str], ...] = (
    ("Pre-2000s", "Domotics and the early ubiquitous-computing vision; X10 home automation."),
    ("2000s", "RFID and wireless sensor networks make low-power sensing practical."),
    ("2010s", "6LoWPAN, CoAP and the Web of Things standardise IP-based IoT."),
    ("2020s", "IoT passes the tipping point; edge AI, federated learning and post-quantum cryptography emerge."),
    ("Future", "Smart dust, battery-less intermittent computing and net-zero resource footprints."),
)

IOT_SOLUTIONS: tuple[tuple[str, str], ...] = (
    ("Edge Computing", "Process telemetry near the source to cut latency, bandwidth and exposure of raw data."),
    ("Lightweight Cryptography", "Use ChaCha20, AES-128 and elliptic-curve primitives sized for constrained MCUs."),
    ("Federated Learning", "Train models locally and share only aggregated updates to preserve privacy."),
    ("Open Standards & RIOT OS", "Build on vendor-independent open source and standard protocols to avoid lock-in."),
)

IOT_STAKEHOLDERS: tuple[tuple[str, str], ...] = (
    ("Governments & Regulators", "Enforce privacy law, fund open standards and require security-by-design procurement."),
    ("Academic & Research Institutions", "Develop lightweight security, benchmark energy use and publish reproducible results."),
    ("Developers & Engineers", "Adopt secure update pipelines, least privilege and energy-aware programming."),
    ("End Users & Consumers", "Demand transparency, maintain devices and prefer products with long support lifetimes."),
)

IOT_TAKEAWAY = (
    "Digital sovereignty and secure-by-design engineering are not optional features: they are "
    "the conditions under which a sustainable IoT can earn and retain public trust."
)
