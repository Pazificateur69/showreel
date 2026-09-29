#!/usr/bin/env python3
"""Génère en/index.html à partir de index.html (FR) et de la table de traduction ci-dessous.

La page française est la seule source : on la modifie, puis `python3 build_en.py`.
Chaque texte doit être trouvé exactement le nombre de fois indiqué, sinon le script s'arrête
(une phrase française modifiée sans sa traduction ne passe donc pas en silence).
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
BASE = 'https://pazificateur69.github.io/showreel/'

JSONLD_EN = ('{"@context":"https://schema.org","@type":"ProfilePage","url":"' + BASE + 'en/","inLanguage":"en",'
             '"mainEntity":{"@type":"Person","name":"Alessandro Gagliardi","jobTitle":"Cybersecurity and DevSecOps engineer",'
             '"description":"Penetration testing, application auditing, hardening, incident response and DevSecOps on production servers.",'
             '"email":"mailto:alessandro.gagliardi225145@gmail.com","address":{"@type":"PostalAddress","addressLocality":"Villeurbanne",'
             '"addressRegion":"Auvergne-Rhône-Alpes","addressCountry":"FR"},"alumniOf":{"@type":"CollegeOrUniversity","name":"Guardia Cybersecurity School"},'
             '"knowsLanguage":["fr","en","it","ru"],"knowsAbout":["Penetration testing","DevSecOps","Linux hardening","Incident response",'
             '"OWASP Top 10","MITRE ATT&CK","EBIOS Risk Manager","LLM security"],"sameAs":["https://github.com/Pazificateur69","https://pazificateur69.github.io/"]}}')

# (texte français, texte anglais, nombre d'occurrences attendu)
T = [
    # ---- En-tête ----
    ('<html lang="fr">', '<html lang="en">', 1),
    ('<title>Alessandro Gagliardi · Ingénieur cybersécurité &amp; DevSecOps à Lyon</title>',
     '<title>Alessandro Gagliardi · Cybersecurity &amp; DevSecOps Engineer in Lyon</title>', 1),
    ('content="Showreel interactif d’Alessandro Gagliardi, ingénieur cybersécurité et DevSecOps à Lyon : pentest, durcissement, réponse à incident, DevSecOps, projets et parcours."',
     'content="Interactive showreel of Alessandro Gagliardi, cybersecurity and DevSecOps engineer in Lyon: penetration testing, hardening, incident response, DevSecOps, projects and career."', 1),
    ('<link rel="canonical" href="' + BASE + '">', '<link rel="canonical" href="' + BASE + 'en/">', 1),
    ('<meta property="og:locale" content="fr_FR">', '<meta property="og:locale" content="en_US">', 1),
    ('<meta property="og:url" content="' + BASE + '">', '<meta property="og:url" content="' + BASE + 'en/">', 1),
    ('<meta property="og:title" content="Alessandro Gagliardi · Ingénieur cybersécurité &amp; DevSecOps à Lyon">',
     '<meta property="og:title" content="Alessandro Gagliardi · Cybersecurity &amp; DevSecOps Engineer in Lyon">', 1),
    ('<meta property="og:description" content="Showreel interactif : pentest, durcissement, réponse à incident, DevSecOps, projets et parcours.">',
     '<meta property="og:description" content="Interactive showreel: penetration testing, hardening, incident response, DevSecOps, projects and career.">', 1),
    ('content="' + BASE + 'og.png"', 'content="' + BASE + 'og-en.png"', 1),
    # ---- HUD ----
    ('<a class="hud-link" href="en/" hreflang="en" lang="en" aria-label="English version">EN</a>',
     '<a class="hud-link" href="../" hreflang="fr" lang="fr" aria-label="Version française">FR</a>', 1),
    ('href="cv-alessandro-gagliardi-fr.pdf"', 'href="../cv-alessandro-gagliardi-en.pdf"', 2),
    ('aria-label="Lecture automatique"', 'aria-label="Autoplay"', 1),
    ('<span class="hud-play-l">Lire</span>', '<span class="hud-play-l">Play</span>', 1),
    ('aria-label="Scènes du showreel"', 'aria-label="Showreel scenes"', 1),
    ('>01 Ouverture<', '>01 Opening<', 2), ('>02 Manifeste<', '>02 Manifesto<', 1), ('>03 Chiffres<', '>03 Numbers<', 1),
    ('>04 Parcours<', '>04 Career<', 1), ('>05 Terrain<', '>05 Field<', 1), ('>06 Projets<', '>06 Projects<', 1),
    ('>08 Générique<', '>08 Credits<', 1),
    ('data-scene="Ouverture"', 'data-scene="Opening"', 1), ('data-scene="Manifeste"', 'data-scene="Manifesto"', 1),
    ('data-scene="Chiffres"', 'data-scene="Numbers"', 1), ('data-scene="Parcours"', 'data-scene="Career"', 1),
    ('data-scene="Terrain"', 'data-scene="Field"', 1), ('data-scene="Projets"', 'data-scene="Projects"', 1),
    ('data-scene="Générique"', 'data-scene="Credits"', 1),
    ('<p class="leader-skip mono">Touche ou clic pour passer</p>', '<p class="leader-skip mono">Press any key or click to skip</p>', 1),
    # ---- Ouverture ----
    ('Ingénieur cybersécurité et DevSecOps à Lyon. Disponible dès la rentrée 2026 pour une alternance, 3&nbsp;semaines en entreprise et 1&nbsp;à l’école.',
     'Cybersecurity and DevSecOps engineer in Lyon. Available from September 2026 for a work-study contract, 3&nbsp;weeks in company and 1&nbsp;at school.', 1),
    ('<span>Lancer le showreel</span>', '<span>Play the showreel</span>', 1),
    ('data-magnetic>Me contacter</a>', 'data-magnetic>Get in touch</a>', 1),
    ('<span>Me contacter</span>', '<span>Get in touch</span>', 1),
    # ---- Manifeste ----
    ('<h2 class="sr-only">Manifeste</h2>', '<h2 class="sr-only">Manifesto</h2>', 1),
    ('<span class="ml-t">J’attaque.</span><span class="ml-c">Pentest web, réseau et système. Bug bounty, CTF, audit de smart contracts.</span>',
     '<span class="ml-t">I attack.</span><span class="ml-c">Web, network and system pentesting. Bug bounty, CTF, smart contract auditing.</span>', 1),
    ('<span class="ml-t">Je durcis.</span><span class="ml-c">Linux, WAF, CrowdSec, supervision, réponse à incident, chaîne CI sécurisée.</span>',
     '<span class="ml-t">I harden.</span><span class="ml-c">Linux, WAF, CrowdSec, monitoring, incident response, secured CI pipeline.</span>', 1),
    ('<span class="ml-t">Je vérifie.</span><span class="ml-c">Persistance des mesures revérifiée deux mois plus tard.</span>',
     '<span class="ml-t">I verify.</span><span class="ml-c">Controls re-verified two months later.</span>', 1),
    ('Profil cybersécurité généraliste, formé sur des environnements de production réels&nbsp;: audit applicatif OWASP, pentest, bug bounty, durcissement Linux, réponse à incident, DevSecOps et conformité RGPD. Je relie l’analyse de risques aux correctifs, et je vérifie qu’ils tiennent dans la durée.',
     'Generalist cybersecurity profile trained on real production environments: OWASP application auditing, penetration testing, bug bounty, Linux hardening, incident response, DevSecOps and GDPR compliance. I connect risk analysis to concrete fixes, and I verify that they hold over time.', 1),
    # ---- Chiffres ----
    ('<h2 class="sr-only">Chiffres clés</h2>', '<h2 class="sr-only">Key figures</h2>', 1),
    ('<p class="beat-unit">vulnérabilités</p>', '<p class="beat-unit">vulnerabilities</p>', 1),
    ('Audit white-box et dynamique d’un SaaS Angular et Laravel, classées OWASP, CWE et CVSS.',
     'White-box and dynamic audit of an Angular and Laravel SaaS, classified against OWASP, CWE and CVSS.', 1),
    ('<span class="sr-only">9,9</span><span class="odo" aria-hidden="true">9,9</span>', '<span class="sr-only">9.9</span><span class="odo" aria-hidden="true">9.9</span>', 1),
    ('<p class="beat-unit">score CVSS</p>', '<p class="beat-unit">CVSS score</p>', 1),
    ('Élévation de privilèges critique trouvée pendant cet audit, avec des IDOR sur 11 contrôleurs et des secrets exposés.',
     'Critical privilege escalation found during that audit, along with IDOR across 11 controllers and exposed secrets.', 1),
    ('<span class="sr-only">15&#8239;000</span><span class="odo" aria-hidden="true">15&#8239;000</span>', '<span class="sr-only">15,000</span><span class="odo" aria-hidden="true">15,000</span>', 1),
    ('<p class="beat-unit">adresses IP bannies</p>', '<p class="beat-unit">IP addresses banned</p>', 1),
    ('CrowdSec et Fail2ban déployés sur un serveur de production Plesk.', 'CrowdSec and Fail2ban deployed on a Plesk production server.', 1),
    ('<span class="sr-only">de 67 à 77</span>', '<span class="sr-only">from 67 to 77</span>', 1),
    ('<p class="beat-unit">score Lynis</p>', '<p class="beat-unit">Lynis score</p>', 1),
    ('Après audit et durcissement du même serveur&nbsp;: 20 risques priorisés, dont 6 critiques, et 9 CVE noyau corrigées à chaud.',
     'After auditing and hardening the same server: 20 risks prioritised, 6 of them critical, and 9 kernel CVEs patched live.', 1),
    ('<span class="sr-only">90,1&nbsp;%</span><span class="odo" aria-hidden="true">90,1</span>', '<span class="sr-only">90.1%</span><span class="odo" aria-hidden="true">90.1</span>', 1),
    ('<p class="beat-unit">benchmark XBEN</p>', '<p class="beat-unit">XBEN benchmark</p>', 1),
    ('Taux de réussite de T3MP3ST, framework offensif piloté par IA auquel j’ai contribué.',
     'Success rate of T3MP3ST, an AI-driven offensive framework I contributed to.', 1),
    ('<span class="sr-only">31&#8239;400</span><span class="odo" aria-hidden="true">31&#8239;400</span>', '<span class="sr-only">31,400</span><span class="odo" aria-hidden="true">31,400</span>', 1),
    ('<p class="beat-unit">lignes de Rust</p>', '<p class="beat-unit">lines of Rust</p>', 1),
    ('CURS3D, blockchain de couche 1 post-quantique&nbsp;: signatures CRYSTALS-Dilithium, consensus BFT à preuve d’enjeu, machine virtuelle WASM.',
     'CURS3D, a post-quantum layer 1 blockchain: CRYSTALS-Dilithium signatures, BFT proof-of-stake consensus, WASM virtual machine.', 1),
    # ---- Parcours ----
    ('<h2 class="career-title">Parcours</h2>', '<h2 class="career-title">Career</h2>', 1),
    ('<p class="career-date" aria-hidden="true">Mars 2023</p>', '<p class="career-date" aria-hidden="true">Mar. 2023</p>', 1),
    ('<span>Moniteur du programme</span><span class="mon-name">Parcours</span>', '<span>Program monitor</span><span class="mon-name">Career</span>', 1),
    ('data-label="Mastère"', 'data-label="Master’s"', 1),
    ('data-label="Distribution et vendanges"', 'data-label="Retail and harvest"', 1),
    ('<h3 class="cc-title">Mastère Cybersécurité, Bac+5</h3>', '<h3 class="cc-title">Master’s in Cybersecurity, Bac+5</h3>', 1),
    ('Guardia Cybersecurity School. 1re année en cours, en alternance&nbsp;: 3&nbsp;semaines en entreprise, 1&nbsp;semaine à l’école.',
     'Guardia Cybersecurity School. First year in progress, work-study: 3&nbsp;weeks in company, 1&nbsp;week at school.', 1),
    ('sept. 2026</span><span>Feyzin (69)</span>', 'Sept. 2026</span><span>Feyzin, France</span>', 1),
    ('<h3 class="cc-title">Alternant cybersécurité et DevSecOps</h3>', '<h3 class="cc-title">Cybersecurity &amp; DevSecOps apprentice</h3>', 1),
    ('NetStrategy, agence web et produits SaaS. Référent sécurité du parc applicatif et des serveurs de production.',
     'NetStrategy, web agency and SaaS products. Security lead for the application portfolio and production servers.', 1),
    ('Audit white-box d’un SaaS Angular et Laravel&nbsp;: 45 vulnérabilités, dont une élévation de privilèges CVSS 9,9.',
     'White-box audit of an Angular and Laravel SaaS: 45 vulnerabilities, including a CVSS 9.9 privilege escalation.', 1),
    ('Trois applications internes sécurisées&nbsp;: CRM Next.js (31 vulnérabilités), app mobile (52 corrections sur 53), app comptable.',
     'Three internal applications secured: Next.js CRM (31 vulnerabilities), mobile app (52 fixes out of 53), accounting app.', 1),
    ('Chaîne DevSecOps en CI&nbsp;: Semgrep, Trivy, Gitleaks, OWASP ZAP, SBOM CycloneDX, signature Cosign, conteneurs distroless.',
     'DevSecOps pipeline in CI: Semgrep, Trivy, Gitleaks, OWASP ZAP, CycloneDX SBOM, Cosign signing, distroless containers.', 1),
    ('Infrastructure Proxmox et OPNsense segmentée, supervisée par Centreon, automatisée avec Ansible.',
     'Segmented Proxmox and OPNsense infrastructure, monitored with Centreon, automated with Ansible.', 1),
    ('<h3 class="cc-title">Bachelor Cybersécurité, Bac+3</h3>', '<h3 class="cc-title">Bachelor’s in Cybersecurity, Bac+3</h3>', 1),
    ('Guardia Cybersecurity School. Diplômé.', 'Guardia Cybersecurity School. Graduated.', 1),
    ('Titre RNCP niveau 6, Administrateur d’Infrastructures Sécurisées (RNCP37680), obtenu en 2026.',
     'Level 6 professional qualification, Secured Infrastructure Administrator (RNCP37680), obtained in 2026.', 1),
    ('Projet de fin d’études DataForge&nbsp;: le SI Zero Trust complet d’une entreprise fictive, sur 7 machines virtuelles.',
     'Final-year project DataForge: the complete Zero Trust IT system of a fictional company, across 7 virtual machines.', 1),
    ('<span>Août 2024 ', '<span>Aug. 2024 ', 1),
    ('juil. 2025</span><span>Chassieu (69)</span>', 'July 2025</span><span>Chassieu, France</span>', 1),
    ('<h3 class="cc-title">Consultant SEO et développeur web</h3>', '<h3 class="cc-title">SEO consultant and web developer</h3>', 1),
    ('Alertis, stage puis freelance.', 'Alertis, internship then freelance.', 1),
    ('Développement et optimisation de sites Shopify et WordPress.', 'Built and optimised Shopify and WordPress sites.', 1),
    ('Automatisation Python et JavaScript, scraping concurrentiel.', 'Python and JavaScript automation, competitive scraping.', 1),
    ('Performance web et Core Web Vitals, en autonomie sur les livrables et la relation client.',
     'Web performance and Core Web Vitals, autonomous on deliverables and client relationship.', 1),
    ('<h3 class="cc-title">Employé polyvalent, vendangeur et pressureur</h3>', '<h3 class="cc-title">Retail associate, grape harvester and press operator</h3>', 1),
    ('Grande distribution et Oedoria, secteur viticole.', 'Retail chain and Oedoria, wine industry.', 1),
    ('Rigueur opérationnelle, continuité d’activité et travail d’équipe en environnement contraint.',
     'Operational rigour, business continuity and teamwork in constrained environments.', 1),
    ('<h3 class="cc-title">Baccalauréat général</h3>', '<h3 class="cc-title">French Baccalauréat</h3>', 1),
    ('Mathématiques, physique-chimie, mathématiques expertes.', 'Science track: mathematics, physics and chemistry, advanced mathematics.', 1),
    ('<span>V2 <em>Formation</em></span><span>V1 <em>Pro</em></span>', '<span>V2 <em>Education</em></span><span>V1 <em>Work</em></span>', 1),
    ('aria-label="à"', 'aria-label="to"', 5),
    # ---- Terrain ----
    ('<h2 class="fp-title">Offensif</h2>', '<h2 class="fp-title">Offensive</h2>', 1),
    ('<h2 class="fp-title">Défensif</h2>', '<h2 class="fp-title">Defensive</h2>', 1),
    ('<h3>Bug bounty sur YesWeHack</h3><p>Deux vulnérabilités de criticité haute chez un opérateur télécom&nbsp;: spécification OpenAPI exposée sans authentification, contournement d’authentification.</p>',
     '<h3>Bug bounty on YesWeHack</h3><p>Two high-severity vulnerabilities at a telecom operator: OpenAPI specification exposed without authentication, and an authentication bypass.</p>', 1),
    ('<h3>Audit de smart contracts sur Code4rena</h3><p>Protocole de prêt en Rust et Soroban&nbsp;: une vulnérabilité moyenne à haute, avec preuve de concept exécutable.</p>',
     '<h3>Smart contract auditing on Code4rena</h3><p>Rust and Soroban lending protocol: a medium-to-high severity finding with an executable proof of concept.</p>', 1),
    ('<h3>CTF et laboratoires</h3><p>Challenge industriel OPC-UA et SCADA sur Root-Me, laboratoire boot2root compromis jusqu’au compte root.</p>',
     '<h3>CTF and labs</h3><p>Industrial OPC-UA and SCADA challenge on Root-Me, full compromise of a boot2root lab up to root access.</p>', 1),
    ('<h3>Audit et durcissement d’un serveur Plesk</h3><p>20 risques identifiés et priorisés, dont 6 critiques, documentés en 11 fiches et 3 runbooks réutilisables (SSH, WAF, Docker).</p>',
     '<h3>Audit and hardening of a Plesk server</h3><p>20 risks identified and prioritised, 6 of them critical, documented across 11 files and 3 reusable runbooks (SSH, WAF, Docker).</p>', 1),
    ('<h3>Défense en profondeur</h3><p>SSH par clé uniquement, ModSecurity et OWASP CRS en blocage, CrowdSec et Fail2ban, 7 ports Docker retirés d’Internet, 9 CVE noyau corrigées à chaud.</p>',
     '<h3>Defence in depth</h3><p>Key-only SSH, ModSecurity and OWASP CRS in blocking mode, CrowdSec and Fail2ban, 7 Docker ports removed from the internet, 9 kernel CVEs patched live.</p>', 1),
    ('<h3>Réponse à incident</h3><p>Tentative d’inclusion de fichier sur /.env contenue, règle Nginx anti-dotfiles sur 15 domaines, TLS sortant activé. Mesures revérifiées deux mois plus tard.</p>',
     '<h3>Incident response</h3><p>File inclusion attempt on /.env contained, Nginx anti-dotfile rule across 15 domains, outbound TLS enabled. Controls re-verified two months later.</p>', 1),
    # ---- Projets ----
    ('<h2 class="big-title">Projets</h2>', '<h2 class="big-title">Projects</h2>', 1),
    ('Huit productions, du framework de pentest à la blockchain post-quantique. Chaque ligne s’ouvre sur son détail et un aperçu animé.',
     'Eight productions, from a pentest framework to a post-quantum blockchain. Each row opens on its details and an animated preview.', 1),
    ('<span class="proj-kind mono">Offensif</span>', '<span class="proj-kind mono">Offensive</span>', 1),
    ('<span class="proj-desc">Framework de pentest open source</span>', '<span class="proj-desc">Open-source pentest framework</span>', 1),
    ('Reconnaissance, tests web et réseau, Active Directory et reporting réunis dans une seule chaîne. 72 modules, validé sur DVWA, Juice Shop et WebGoat.',
     'Reconnaissance, web and network testing, Active Directory and reporting in a single chain. 72 modules, validated against DVWA, Juice Shop and WebGoat.', 1),
    ('>Code source <svg', '>Source code <svg', 4),
    ('<span class="proj-kind mono">IA offensive</span>', '<span class="proj-kind mono">Offensive AI</span>', 1),
    ('<span class="proj-desc">Framework offensif piloté par IA</span>', '<span class="proj-desc">AI-driven offensive framework</span>', 1),
    ('<span class="proj-metric mono">90,1&nbsp;% XBEN</span>', '<span class="proj-metric mono">90.1% XBEN</span>', 1),
    ('Contribution à un outil où des agents autonomes enchaînent reconnaissance, exploitation et rapport, selon une kill chain mappée MITRE ATT&amp;CK. 90,1&nbsp;% de réussite sur le benchmark XBEN.',
     'Contribution to a tool where autonomous agents chain reconnaissance, exploitation and reporting along a kill chain mapped to MITRE ATT&amp;CK. 90.1% success rate on the XBEN benchmark.', 1),
    ('Agents IA / MITRE ATT&amp;CK / Red team', 'AI agents / MITRE ATT&amp;CK / Red team', 1),
    ('<span class="proj-kind mono">Infra Zero Trust</span>', '<span class="proj-kind mono">Zero Trust infra</span>', 1),
    ('<span class="proj-desc">Système d’information Zero Trust</span>', '<span class="proj-desc">Zero Trust information system</span>', 1),
    ('<span class="proj-metric mono">7 VM</span>', '<span class="proj-metric mono">7 VMs</span>', 1),
    ('Projet de fin d’études&nbsp;: le SI complet d’une entreprise fictive sur 7 machines virtuelles. Active Directory, WireGuard, nftables en refus par défaut, Wazuh et Suricata, analyse EBIOS RM.',
     'Final-year project: the complete IT system of a fictional company across 7 virtual machines. Active Directory, WireGuard, deny-by-default nftables, Wazuh and Suricata, EBIOS RM risk analysis.', 1),
    ('<span class="proj-desc">Exécution de code hostile en bac à sable</span>', '<span class="proj-desc">Hostile code execution sandbox</span>', 1),
    ('Plateforme qui exécute du code non fiable dans des conteneurs éphémères&nbsp;: liste blanche d’appels système seccomp, quotas cgroups, fichiers en lecture seule et réseau coupé.',
     'Platform running untrusted code in ephemeral containers: seccomp syscall allow-list, cgroup quotas, read-only filesystem and disabled networking.', 1),
    ('<span class="proj-desc">Blockchain L1 post-quantique</span>', '<span class="proj-desc">Post-quantum layer 1 blockchain</span>', 1),
    ('<span class="proj-metric mono">31&#8239;400 lignes</span>', '<span class="proj-metric mono">31,400 lines</span>', 1),
    ('Blockchain de couche 1 écrite en Rust, avec des signatures résistantes au quantique CRYSTALS-Dilithium. Consensus BFT à preuve d’enjeu, machine virtuelle WASM.',
     'Layer 1 blockchain written in Rust with quantum-resistant CRYSTALS-Dilithium signatures. BFT proof-of-stake consensus, WASM virtual machine.', 1),
    ('Rust / Post-quantique / WASM', 'Rust / Post-quantum / WASM', 1),
    ('<span class="proj-kind mono">Données</span>', '<span class="proj-kind mono">Data</span>', 1),
    ('<span class="roll" data-t="Coffre RGPD">Coffre RGPD</span>', '<span class="roll" data-t="GDPR Vault">GDPR Vault</span>', 1),
    ('<span class="proj-desc">Stockage chiffré de données personnelles</span>', '<span class="proj-desc">Encrypted personal data storage</span>', 1),
    ('Données chiffrées en AES-256-GCM dans le navigateur, registre des consentements, journal d’audit, et effacement par destruction de la clé pour le droit à l’oubli.',
     'Data encrypted with AES-256-GCM in the browser, with a consent registry, audit log and erasure by key destruction to honour the right to be forgotten.', 1),
    ('RGPD / Chiffrement / Crypto-shredding', 'GDPR / Encryption / Crypto-shredding', 1),
    ('<span class="proj-kind mono">Audit Web3</span>', '<span class="proj-kind mono">Web3 audit</span>', 1),
    ('<span class="proj-desc">Méthodologie d’audit de smart contracts</span>', '<span class="proj-desc">Smart contract audit methodology</span>', 1),
    ('Kit de revue de code Solidity&nbsp;: 26 modules d’analyse, checklist de 80 classes de vulnérabilités connues et preuves de concept rejouant des exploits historiques.',
     'Solidity code review kit: 26 analysis modules, a checklist of 80 known vulnerability classes and proofs of concept replaying historical exploits.', 1),
    ('<span class="proj-kind mono">DeFi en production</span>', '<span class="proj-kind mono">DeFi in production</span>', 1),
    ('<span class="proj-desc">Stablecoin déployé en production</span>', '<span class="proj-desc">Stablecoin deployed in production</span>', 1),
    ('Jeton ERC-20 indexé sur le dirham des Émirats, déployé et vérifié publiquement sur Arbitrum One. Proxy évolutif OpenZeppelin, oracle Chainlink et tests de sécurité Hardhat.',
     'ERC-20 token pegged to the UAE dirham, deployed and publicly verified on Arbitrum One. OpenZeppelin upgradeable proxy, Chainlink price oracle and Hardhat security tests.', 1),
    # ---- Arsenal ----
    ('Les outils et référentiels que j’utilise en production, en audit et en laboratoire.', 'The tools and frameworks I use in production, in audits and in the lab.', 1),
    ('<i></i>Offensif</p>', '<i></i>Offensive</p>', 1), ('<i></i>Défense</p>', '<i></i>Defence</p>', 1),
    ('<i></i>Infra et réseau</p>', '<i></i>Infra and network</p>', 1), ('<i></i>Gouvernance</p>', '<i></i>Governance</p>', 1),
    ('<i></i>Sécurité de l’IA</p>', '<i></i>AI security</p>', 1), ('<i></i>Développement</p>', '<i></i>Development</p>', 1),
    ('<li>Pentest web, réseau, système</li>', '<li>Web, network, system pentest</li>', 1), ('<li>Revue de code</li>', '<li>Code review</li>', 1),
    ('<li>Durcissement Linux</li>', '<li>Linux hardening</li>', 1), ('<li>Analyse de logs</li>', '<li>Log analysis</li>', 1),
    ('<li>Veille CVE</li>', '<li>CVE monitoring</li>', 1), ('<li>SBOM CycloneDX</li>', '<li>CycloneDX SBOM</li>', 1),
    ('<li>Docker non-root</li>', '<li>Non-root Docker</li>', 1), ('<li>RGPD</li>', '<li>GDPR</li>', 1),
    ('<li>Threat modeling</li>', '<li>Threat modelling</li>', 1), ('<li>PCA et PRA</li>', '<li>BCP and DRP</li>', 1),
    ('<li>PKI et X.509</li>', '<li>PKI and X.509</li>', 1), ('<li>Injection de prompt</li>', '<li>Prompt injection</li>', 1),
    ('<li>Jailbreak</li>', '<li>Jailbreaking</li>', 1), ('<li>Red teaming de LLM</li>', '<li>LLM red teaming</li>', 1),
    ('<li>Durcissement de prompts système</li>', '<li>System prompt hardening</li>', 1), ('<li>Garde-fous</li>', '<li>Guardrails</li>', 1),
    ('<li>Orchestration d’agents</li>', '<li>Agent orchestration</li>', 1), ('<li>Protocole MCP</li>', '<li>MCP protocol</li>', 1),
    ('<li>Exemples adversariaux</li>', '<li>Adversarial examples</li>', 1), ('<li>PHP et Laravel</li>', '<li>PHP and Laravel</li>', 1),
    # ---- Générique, contact, fin ----
    ('<h2 class="sr-only">Générique</h2>', '<h2 class="sr-only">Credits</h2>', 1),
    ('<p class="cr-pre mono">Un film de</p>', '<p class="cr-pre mono">A film by</p>', 1),
    ('<dt>Réalisation</dt>', '<dt>Directed by</dt>', 1), ('<dt>Sécurité offensive</dt>', '<dt>Offensive security</dt>', 1),
    ('<dt>Sécurité défensive</dt>', '<dt>Defensive security</dt>', 1), ('<dt>Formation</dt>', '<dt>Education</dt>', 1),
    ('<dt>Titre professionnel</dt><dd>Administrateur d’Infrastructures Sécurisées, RNCP niveau 6</dd>',
     '<dt>Professional title</dt><dd>Secured Infrastructure Administrator, RNCP level 6</dd>', 1),
    ('<dt>Langues</dt><dd>Français, anglais C1 (TOEIC), italien B2, russe (notions)</dd>',
     '<dt>Languages</dt><dd>French (native), English C1 (TOEIC), Italian B2, Russian (basic)</dd>', 1),
    ('<dt>Tournage</dt><dd>Villeurbanne et Lyon, mobilité France, télétravail</dd>',
     '<dt>Filmed in</dt><dd>Villeurbanne and Lyon, open to relocation within France and remote work</dd>', 1),
    ('<dd>Permis B, véhiculé</dd>', '<dd>Full driving licence, own vehicle</dd>', 1),
    ('<dt>Avec la participation de</dt>', '<dt>Featuring</dt>', 1), ('<dt>Plateformes</dt>', '<dt>Platforms</dt>', 1),
    ('Aucun serveur de production n’a été maltraité pendant le tournage.', 'No production servers were harmed in the making of this film.', 1),
    ('Tournons la <em>suite</em> ensemble.', 'Let’s shoot the <em>sequel</em> together.', 1),
    ('<span>Copier l’adresse</span>', '<span>Copy address</span>', 1),
    ('<span>Télécharger le CV</span>', '<span>Download CV</span>', 1),
    ('<p class="fin-word">Fin</p>', '<p class="fin-word">The End</p>', 1),
    ('font-size: clamp(4rem, 13vw, 12rem); line-height: .8; text-transform: uppercase; font-variation-settings: "wdth" 70;',
     'font-size: clamp(2.6rem, 8.5vw, 8rem); line-height: .8; text-transform: uppercase; font-variation-settings: "wdth" 70;', 1),
    ('<span>Rembobiner</span>', '<span>Rewind</span>', 1),
    # ---- Textes du script ----
    ("['Janv.', 'Févr.', 'Mars', 'Avr.', 'Mai', 'Juin', 'Juil.', 'Août', 'Sept.', 'Oct.', 'Nov.', 'Déc.']",
     "['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']", 1),
    ("hudPlayL.textContent = v ? 'Pause' : 'Lire';", "hudPlayL.textContent = v ? 'Pause' : 'Play';", 1),
    ("label.textContent = ok ? 'Adresse copiée' : 'Adresse sélectionnée';", "label.textContent = ok ? 'Address copied' : 'Address selected';", 1),
    ("status.textContent = ok ? 'Adresse e-mail copiée dans le presse-papiers.' : 'Adresse sélectionnée : copiez-la avec Cmd+C ou Ctrl+C.';",
     "status.textContent = ok ? 'Email address copied to the clipboard.' : 'Address selected: copy it with Cmd+C or Ctrl+C.';", 1),
    ("label.textContent = 'Copier l’adresse';", "label.textContent = 'Copy address';", 1),
    (".toFixed(1).replace('.', ',')", '.toFixed(1)', 2),
    ("'72 MODULES  RECON > RAPPORT'", "'72 MODULES  RECON > REPORT'", 1),
    ("names = ['RECON', 'EXPLOIT', 'RAPPORT']", "names = ['RECON', 'EXPLOIT', 'REPORT']", 1),
    ("'AGENTS AUTONOMES  MITRE ATT&CK'", "'AUTONOMOUS AGENTS  MITRE ATT&CK'", 1),
    ("'7 VM  NFTABLES EN REFUS PAR DÉFAUT'", "'7 VMS  DENY-BY-DEFAULT NFTABLES'", 1),
    ("'SECCOMP  CGROUPS  RÉSEAU COUPÉ'", "'SECCOMP  CGROUPS  NETWORK OFF'", 1),
    ("['nom       Durand', 'email     l.durand@', 'consent.  oui 03-2026', 'adresse   Lyon 3e']",
     "['name      Durand', 'email     l.durand@', 'consent   yes 03-2026', 'address   Lyon 3e']", 1),
    ("'CLÉ DÉTRUITE'", "'KEY DESTROYED'", 1),
    ("'CHIFFREMENT CÔTÉ NAVIGATEUR'", "'IN-BROWSER ENCRYPTION'", 1),
    ("'26 MODULES  PoC D’EXPLOITS HISTORIQUES'", "'26 MODULES  HISTORICAL EXPLOIT PoCs'", 1),
]


def main():
    s = (ROOT / 'index.html').read_text(encoding='utf-8')
    s, n = re.subn(r'(<script type="application/ld\+json">\n).*?(\n</script>)', lambda m: m.group(1) + JSONLD_EN + m.group(2), s, count=1, flags=re.S)
    errors = [] if n == 1 else ['bloc JSON-LD introuvable']
    for fr, en, count in T:
        found = s.count(fr)
        if found != count:
            errors.append(f'{found}x au lieu de {count}x : {fr[:80]}')
            continue
        s = s.replace(fr, en)
    if errors:
        sys.exit('Traduction incomplète :\n  ' + '\n  '.join(errors))
    out = ROOT / 'en' / 'index.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(s, encoding='utf-8')
    print(f'{out.relative_to(ROOT)} écrit ({len(T)} traductions appliquées)')


if __name__ == '__main__':
    main()
