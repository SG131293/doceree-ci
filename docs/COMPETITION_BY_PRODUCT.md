# Doceree Competition Map — Split by Product, with URL Registry

**Document type:** Competitive landscape / product-by-product competitor split / CI Command Center seed input
**Company:** Doceree
**Primary owner:** Sherry George, Product Marketing
**Generated date:** 2026-05-07
**Purpose:** Create the most complete product-by-product competitor file for Doceree, with direct competitors, adjacent competitors, watchlist competitors, official URLs, monitoring URLs, source-monitoring guidance, signal rules, and Codex-ready seed data.
**Critical user correction applied:** `Lasso` / `Lasso (an IQVIA business)` should be treated as **IQVIA Digital** going forward. Use **IQVIA Digital** as the active competitor label; preserve Lasso only as a legacy alias.

---

## Read This First

This file is designed to become `docs/COMPETITION_BY_PRODUCT.md` in the Doceree Competitive Intelligence Command Center repo. It complements `docs/PRODUCT_SPINE.md`, not replaces it.

### Non-negotiable Competition Rules

1. **Do not mix Doceree product truth with competitor claims.** Competitor descriptions are external evidence or analyst interpretation, not Doceree messaging.
2. **Split competitors by product and by threat type.** A competitor can be high overlap for one product and low overlap for another.
3. **Severity and confidence are separate.** A large competitor may have low-confidence evidence; a small competitor may have high-confidence product evidence.
4. **Job posts, patents, social posts, SEO pages, and analyst commentary are directional.** They cannot prove launches without official confirmation.
5. **RepTwin requires a dedicated agentic-AI watchlist.** The category is moving quickly and includes direct pharma engagement platforms, healthcare AI-agent platforms, CRM/platform incumbents, and services/productized AI frameworks.
6. **Use IQVIA Digital, not Lasso, as the active competitor name.** Keep `Lasso`, `Lasso Platform`, `Lasso (an IQVIA business)`, and `IQVIA Lasso` as aliases for matching historical content.
7. **For the CI Command Center, every product competitor entry should eventually map to sources, cadence, evidence strength, monitoring agent, and review routing.**

---

## Source Basis and Research Notes

- Internal source basis: Doceree Product Master Spine and Master Product Requirements Document, including the Competitor & Source Registry v1 and the AI-ready competitor JSON.
- Product architecture source basis: the Product Spine defines Doceree as a connected healthcare-marketing operating system spanning demand-side and supply-side products, with source-status discipline across Confirmed / Inferred / Needs confirmation claims.
- Competitor registry source basis: the Competitor & Source Registry v1 defines competitors, tiers, source lists, monitoring cadence, source-confidence rules, and a 50-source MVP monitoring cohort.
- External research basis: web research was used only to update current naming, especially IQVIA Digital, and to expand the RepTwin agentic-AI competitor set.

### External Research Links Used

- IQVIA Digital: https://www.iqviadigital.com/
- Synthio Labs: https://synthiolabs.com/
- Hippocratic AI: https://hippocraticai.com/
- RoseRx: https://www.roserx.ai/
- PrescriberPoint / Prescriber.AI: https://business.prescriberpoint.com/
- Salesforce Agentforce for Life Sciences: https://www.salesforce.com/life-sciences/artificial-intelligence/
- Veeva AI for Vault CRM: https://www.veeva.com/products/crm-suite/veeva-ai-for-vault-crm/
- Aktana / PharmaForceIQ: https://www.aktana.com/
- Openhelix: https://www.openhelix.co/
- MathCo RepGPT: https://mathco.com/article/sales-rep-assistant-repgpt-intelligent-multi-agent-ai-for-pharma-sales-built-on-databricks/
- Agilisium Pharma Rep Copilot: https://www.agilisium.com/blogs/beyond-traditional-sales-how-ai-agents-are-transforming-hcp-engagement-in-life-sciences
- Arma Partners on Lasso sale to IQVIA: https://www.armapartners.com/deals/arma-partners-advises-lasso-a-leading-omnichannel-healthcare-marketing-and-analytics-platform-on-its-sale-to-iqvia/
- IQVIA homepage / AI context: https://www.iqvia.com/
- Salesforce Agentforce for Life Sciences: https://www.salesforce.com/life-sciences/artificial-intelligence/
- Veeva AI for Vault CRM: https://www.veeva.com/products/crm-suite/veeva-ai-for-vault-crm/
- PharmaForceIQ / Aktana acquisition context: https://pharmaforceiq.com/pharmaforceiq-acquires-aktana/

---

## Comprehensive Competitor URL Registry

Use this registry as the canonical URL layer for `docs/COMPETITION_BY_PRODUCT.md`. The product-level sections below now include `Primary URL` and `Key URLs to Monitor` columns, while this registry preserves deeper monitoring notes. URLs should still be revalidated during source seeding because competitor websites, newsroom paths, careers boards, and acquisition/rebrand redirects can change.

### URL Governance Rules

1. **Official source first.** Prefer competitor-owned homepages, product pages, newsrooms, blogs, careers pages, investor pages, and official docs.
2. **Do not invent missing URLs.** If a URL cannot be verified, mark it `Needs validation` or `Needs source discovery`.
3. **LinkedIn and executive social URLs are manual-only.** They may be stored for reference, but not crawled through browser automation.
4. **News/PR mirrors are secondary.** Use PR Newswire, BusinessWire, GlobeNewswire, investor mirrors, and business publications only when official pages do not exist or for corroboration.
5. **Composite competitors must retain component URLs.** Example: `RedSail Technologies / PioneerRx` uses both parent and product-brand URLs.

| Competitor | Official URL | Key URLs to Monitor | URL Confidence | Monitoring Notes |
|---|---|---|---|---|
| 6sense | [https://6sense.com/](https://6sense.com/) | [1](https://6sense.com/newsroom/)<br>[2](https://6sense.com/product/)<br>[3](https://6sense.com/careers/) | High / verify before seed | Generic B2B ABM/revenue AI platform; healthcare adjacency only. |
| AdButler | [https://www.adbutler.com/](https://www.adbutler.com/) | [1](https://www.adbutler.com/display-ad-server/)<br>[2](https://help.adbutler.com/) | High / verify before seed | Ad server and retail media platform. |
| Agilisium Pharma Rep Copilot | [https://www.agilisium.com/blogs/beyond-traditional-sales-how-ai-agents-are-transforming-hcp-engagement-in-life-sciences](https://www.agilisium.com/blogs/beyond-traditional-sales-how-ai-agents-are-transforming-hcp-engagement-in-life-sciences) | [1](https://www.agilisium.com/blogs/beyond-traditional-sales-how-ai-agents-are-transforming-hcp-engagement-in-life-sciences)<br>[2](https://www.agilisium.com/) | High / verify before seed | Productized services/content around AI agents for pharma HCP engagement. |
| Aktana / PharmaForceIQ | [https://pharmaforceiq.com/](https://pharmaforceiq.com/) | [1](https://www.aktana.com/)<br>[2](https://pharmaforceiq.com/pharmaforceiq-acquires-aktana/) | High / verify before seed | Life sciences commercial/medical AI orchestration; Aktana now under PharmaForceIQ context. |
| AssistRx | [https://www.assistrx.com/](https://www.assistrx.com/) | [1](https://www.assistrx.com/specialty-pharmaceutical-solutions/)<br>[2](https://www.assistrx.com/specialty-pharmaceutical-solutions/assistrx-patient-solutions/)<br>[3](https://www.assistrx.com/careers) | High / verify before seed | Specialty pharma patient access and support services. |
| CCC | [https://www.copyright.com/](https://www.copyright.com/) | [1](https://www.copyright.com/solutions/)<br>[2](https://www.copyright.com/news/) | High / verify before seed | Copyright Clearance Center; content licensing infrastructure. |
| CheckedUp | [https://www.checkedup.com/](https://www.checkedup.com/) | [1](https://www.checkedup.com/solutions/)<br>[2](https://www.checkedup.com/about-us/) | High / verify before seed | Point-of-care screens and patient engagement. |
| ConnectiveRx | [https://www.connectiverx.com/](https://www.connectiverx.com/) | [1](https://www.connectiverx.com/)<br>[2](https://www.connectiverx.com/careers)<br>[3](https://careers-connectiverx.icims.com/jobs/intro?mobile=true&needsRedirect=false) | High / verify before seed | Patient access, copay, hub/support, affordability and adherence. |
| CoverMyMeds | [https://www.covermymeds.health/](https://www.covermymeds.health/) | [1](https://www.covermymeds.health/our-solutions)<br>[2](https://www.covermymeds.health/about/newsroom)<br>[3](https://talentcommunity.mckesson.com/flows/cmm) | High / verify before seed | Medication access, affordability, prior authorization, patient support. |
| Dappier | [https://dappier.com/](https://dappier.com/) | [1](https://dappier.com/)<br>[2](https://docs.dappier.com/publish-and-monetize) | High / verify before seed | AI content monetization, RAG/answering/copilot monetization for publishers. |
| DeepIntent | [https://deepintent.com/](https://deepintent.com/) | [1](https://deepintent.com/news)<br>[2](https://deepintent.com/careers)<br>[3](https://deepintent.com/solutions) | High / verify before seed | Healthcare DSP, Cortex, Helix, HCP/programmatic activation. |
| DeepIntent via Place Exchange | [https://deepintent.com/](https://deepintent.com/) | [1](https://www.placeexchange.com/)<br>[2](https://deepintent.com/news) | High / verify before seed | Composite tracking for DeepIntent DOOH exposure via Place Exchange. |
| Definitive Healthcare | [https://www.definitivehc.com/](https://www.definitivehc.com/) | [1](https://www.definitivehc.com/solutions)<br>[2](https://www.definitivehc.com/blog)<br>[3](https://www.definitivehc.com/about/careers) | High / verify before seed | Healthcare commercial intelligence, provider/account data. |
| Demandbase | [https://www.demandbase.com/](https://www.demandbase.com/) | [1](https://www.demandbase.com/products/account-based-experience/)<br>[2](https://www.demandbase.com/about-us/news/)<br>[3](https://www.demandbase.com/careers/) | High / verify before seed | Generic ABM/revenue platform; healthcare adjacency only. |
| Doximity | [https://www.doximity.com/](https://www.doximity.com/) | [1](https://www.doximity.com/marketing-solutions)<br>[2](https://press.doximity.com/)<br>[3](https://www.doximity.com/careers) | High / verify before seed | HCP destination network, marketing solutions, AI/clinical tools, news/press. |
| DrFirst | [https://drfirst.com/](https://drfirst.com/) | [1](https://drfirst.com/solutions/)<br>[2](https://drfirst.com/news/)<br>[3](https://drfirst.com/careers/) | High / verify before seed | e-prescribing, medication management, patient access adjacency. |
| GoodRx | [https://www.goodrx.com/](https://www.goodrx.com/) | [1](https://investors.goodrx.com/news-and-events/press-releases)<br>[2](https://www.goodrx.com/about/careers) | High / verify before seed | Prescription savings, pharma solutions, DTP affordability, investor news. |
| Google Ad Manager | [https://admanager.google.com/home/](https://admanager.google.com/home/) | [1](https://admanager.google.com/home/)<br>[2](https://support.google.com/admanager/)<br>[3](https://publishersonair.withgoogle.com/ad-manager-getting-started) | High / verify before seed | Publisher ad management benchmark. |
| Haymarket / M3 / Everyday Health Professional | [https://www.haymarketmedia.com/](https://www.haymarketmedia.com/) | [1](https://corporate.m3.com/)<br>[2](https://www.everydayhealthgroup.com/)<br>[3](https://www.haymarketmedicalnetwork.com/) | High / verify before seed | Composite HCP/professional media watchlist; validate exact property by market. |
| Hippocratic AI | [https://hippocraticai.com/](https://hippocraticai.com/) | [1](https://hippocraticai.com/lifesciences/)<br>[2](https://hippocraticai.com/healthcare-agents/)<br>[3](https://hippocraticai.com/view-all-agents/) | High / verify before seed | Healthcare generative AI agents; pharma/life-sciences category watchlist. |
| IQVIA | [https://www.iqvia.com/](https://www.iqvia.com/) | [1](https://www.iqvia.com/newsroom)<br>[2](https://www.iqvia.com/solutions)<br>[3](https://iqvia.wd1.myworkdayjobs.com/IQVIA/) | High / verify before seed | Global healthcare data, analytics, clinical/commercial technology; monitor IQVIA.ai, commercial data, digital marketing and AI moves. |
| IQVIA Digital | [https://www.iqviadigital.com/](https://www.iqviadigital.com/) | [1](https://www.iqviadigital.com/solutions)<br>[2](https://www.iqviadigital.com/resources)<br>[3](https://www.iqviadigital.com/about-us/careers)<br>[4](https://www.iqviadigital.com/client-portals) | High / verify before seed | Active label replacing Lasso; monitor solutions/resources/client portals and IQVIA integration. |
| Kevel | [https://www.kevel.com/](https://www.kevel.com/) | [1](https://www.kevel.com/ad-server)<br>[2](https://dev.kevel.com/reference/getting-started-with-kevel) | High / verify before seed | API ad serving / retail media infrastructure. |
| Komodo Health | [https://www.komodohealth.com/](https://www.komodohealth.com/) | [1](https://www.komodohealth.com/solutions)<br>[2](https://www.komodohealth.com/insights)<br>[3](https://www.komodohealth.com/careers/life-at-komodo/) | High / verify before seed | Healthcare Map, RWD, analytics, MapLab, AI-enabled life-sciences insights. |
| Magnite | [https://www.magnite.com/](https://www.magnite.com/) | [1](https://www.magnite.com/press/)<br>[2](https://www.magnite.com/about-us/) | High / verify before seed | Independent sell-side advertising platform. |
| MathCo RepGPT | [https://mathco.com/article/sales-rep-assistant-repgpt-intelligent-multi-agent-ai-for-pharma-sales-built-on-databricks/](https://mathco.com/article/sales-rep-assistant-repgpt-intelligent-multi-agent-ai-for-pharma-sales-built-on-databricks/) | [1](https://mathco.com/article/sales-rep-assistant-repgpt-intelligent-multi-agent-ai-for-pharma-sales-built-on-databricks/)<br>[2](https://mathco.com/) | High / verify before seed | RepGPT multi-agent pharma sales assistant concept. |
| MedAdvisor | [https://www.medadvisor.com/](https://www.medadvisor.com/) | [1](https://www.medadvisor.com/)<br>[2](https://www.medadvisor.com/news/) | High / verify before seed | Pharmacy/patient engagement/adherence; validate regional relevance. |
| Medscape (WebMD Health) | [https://www.medscapeglobal.com/](https://www.medscapeglobal.com/) | [1](https://www.medscape.com/)<br>[2](https://www.webmd.com/mediakit)<br>[3](https://jobs.jobvite.com/webmd/jobs) | High / verify before seed | Medscape/WebMD professional media and HCP engagement. |
| Medscape / WebMD Health | [https://www.medscapeglobal.com/](https://www.medscapeglobal.com/) | [1](https://www.medscape.com/)<br>[2](https://www.webmd.com/mediakit)<br>[3](https://jobs.jobvite.com/webmd/jobs) | High / verify before seed | Same entity grouping as Medscape (WebMD Health). |
| OpenEvidence | [https://www.openevidence.com/](https://www.openevidence.com/) | [1](https://www.openevidence.com/) | High / verify before seed | AI for doctors / clinical evidence; monitor pharma-facing or HCP engagement expansion. |
| Openhelix | [https://www.openhelix.co/](https://www.openhelix.co/) | [1](https://www.openhelix.co/) | High / verify before seed | Healthcare/life sciences AI-agent watchlist. |
| OptimizeRx | [https://www.optimizerx.com/](https://www.optimizerx.com/) | [1](https://investors.optimizerx.com/news-releases)<br>[2](https://www.optimizerx.com/blog)<br>[3](https://www.optimizerx.com/careers) | High / verify before seed | POC/EHR engagement, patient/provider messaging, digital activation, investor news. |
| Outbrain | [https://www.outbrain.com/](https://www.outbrain.com/) | [1](https://www.outbrain.com/advertisers/)<br>[2](https://www.outbrain.com/blog/)<br>[3](https://www.outbrain.com/careers/) | High / verify before seed | Native/content discovery advertising, adjacent to content marketing. |
| PatientPoint | [https://patientpoint.com/](https://patientpoint.com/) | [1](https://careers.patientpoint.com/)<br>[2](https://careers.patientpoint.com/search/searchjobs)<br>[3](https://patientpoint.com/) | High / verify before seed | Point-of-care digital screens and patient/HCP engagement network. |
| Place Exchange | [https://www.placeexchange.com/](https://www.placeexchange.com/) | [1](https://www.placeexchange.com/news)<br>[2](https://www.placeexchange.com/about) | High / verify before seed | Programmatic OOH exchange; monitor DOOH partnerships. |
| PrescriberPoint | [https://prescriberpoint.com/](https://prescriberpoint.com/) | [1](https://prescriberpoint.com/prescriber-ai)<br>[2](https://prescriberpoint.com/insights/introducing-prescriberai)<br>[3](https://prescriberpointwebapps.com/signup) | High / verify before seed | AI-powered point-of-care prescribing workflow platform; PrescriberAI. |
| PrescriberPoint / Prescriber.AI | [https://prescriberpoint.com/](https://prescriberpoint.com/) | [1](https://prescriberpoint.com/prescriber-ai)<br>[2](https://prescriberpoint.com/insights/introducing-prescriberai) | High / verify before seed | Alias grouping for PrescriberPoint and PrescriberAI. |
| PubMatic | [https://pubmatic.com/](https://pubmatic.com/) | [1](https://pubmatic.com/about-us/)<br>[2](https://pubmatic.com/news/)<br>[3](https://pubmatic.com/solutions/mobile/) | High / verify before seed | SSP / publisher monetization and AI-powered ad platform. |
| PulsePoint | [https://www.pulsepoint.com/](https://www.pulsepoint.com/) | [1](https://www.pulsepoint.com/resources/newsroom)<br>[2](https://blog.pulsepoint.com/)<br>[3](https://jobs.jobvite.com/pulsepoint/jobs) | High / verify before seed | Healthcare programmatic, HCP365, EHR/programmatic partnerships, WebMD/Internet Brands adjacency. |
| RedSail Technologies | [https://www.redsailtechnologies.com/](https://www.redsailtechnologies.com/) | [1](https://www.redsailtechnologies.com/press-releases)<br>[2](https://www.pioneerrx.com/category/press-releases)<br>[3](https://www.redsailtechnologies.com/careers) | High / verify before seed | Pharmacy management systems; PioneerRx, QS/1, pharmacy network. |
| RedSail Technologies / PioneerRx | [https://www.redsailtechnologies.com/](https://www.redsailtechnologies.com/) | [1](https://www.pioneerrx.com/)<br>[2](https://www.pioneerrx.com/category/press-releases)<br>[3](https://www.redsailtechnologies.com/press-releases) | High / verify before seed | Use RedSail as parent; PioneerRx as product/brand alias. |
| RelayHealth / Change Healthcare / Optum Insight | [https://business.optum.com/en/optum-insight.html](https://business.optum.com/en/optum-insight.html) | [1](https://www.changehealthcare.com/)<br>[2](https://business.optum.com/en/optum-insight.html)<br>[3](https://www.optum.com/en/about-us/careers.html) | High / verify before seed | Use Optum Insight / Change Healthcare as current grouping; RelayHealth is legacy context. |
| Relevate Health | [https://www.relevatehealth.com/](https://www.relevatehealth.com/) | [1](https://www.relevatehealth.com/news)<br>[2](https://www.relevatehealth.com/blogs/enhancing-hcp-customer-experience-within-the-ehr-workflow)<br>[3](https://www.relevatehealth.com/careers) | High / verify before seed | HCP omnichannel campaigns, EHR workflow-triggered messaging, Level Ex games. |
| RoseRx | [https://www.roserx.ai/](https://www.roserx.ai/) | [1](https://www.roserx.ai/hcp-engagement-platform)<br>[2](https://www.roserx.ai/about)<br>[3](https://www.roserx.ai/contact) | High / verify before seed | AI-powered pharma HCP/patient engagement platform. |
| Salesforce Agentforce for Life Sciences | [https://www.salesforce.com/life-sciences/artificial-intelligence/](https://www.salesforce.com/life-sciences/artificial-intelligence/) | [1](https://www.salesforce.com/life-sciences/artificial-intelligence/)<br>[2](https://www.salesforce.com/news/)<br>[3](https://www.salesforce.com/products/agentforce/) | High / verify before seed | Platform incumbent; life sciences agentic AI and CRM workflow adjacency. |
| Screenverse | [https://www.screenversemedia.com/](https://www.screenversemedia.com/) | [1](https://www.screenversemedia.com/services/digital-billboards)<br>[2](https://www.screenversemedia.com/blog) | High / verify before seed | Programmatic DOOH network/monetization. |
| Smaato | [https://www.smaato.com/](https://www.smaato.com/) | [1](https://www.smaato.com/company/)<br>[2](https://www.smaato.com/publishers/)<br>[3](https://verve.com/brand-marketplace-for-publishers/) | High / verify before seed | Now framed as Verve Brand+ Marketplace; mobile/omnichannel ad monetization. |
| StackAdapt | [https://www.stackadapt.com/](https://www.stackadapt.com/) | [1](https://www.stackadapt.com/our-solutions/npi-targeting-and-measurement)<br>[2](https://www.stackadapt.com/resources)<br>[3](https://www.stackadapt.com/careers) | High / verify before seed | Programmatic platform with NPI targeting/measurement and healthcare advertising signals. |
| Surescripts | [https://surescripts.com/](https://surescripts.com/) | [1](https://surescripts.com/solutions)<br>[2](https://surescripts.com/news-center)<br>[3](https://surescripts.com/careers) | High / verify before seed | E-prescribing/network infrastructure, benefits, medication history and pharmacy workflow adjacency. |
| Swoop | [https://swoop.com/](https://swoop.com/) | [1](https://swoop.com/)<br>[2](https://ats.rippling.com/swoopishiring/jobs) | High / verify before seed | AI/data-powered healthcare omnichannel marketing and predictive audiences. |
| Synthio Labs | [https://synthiolabs.com/](https://synthiolabs.com/) | [1](https://synthiolabs.com/) | High / verify before seed | Agentic AI platform for pharma GTM / field, HCP, patient engagement agents. |
| Taboola | [https://www.taboola.com/](https://www.taboola.com/) | [1](https://www.taboola.com/advertisers)<br>[2](https://www.taboola.com/resources)<br>[3](https://www.taboola.com/careers) | High / verify before seed | Native/content discovery advertising, adjacent to content marketing. |
| TollBit | [https://tollbit.com/](https://tollbit.com/) | [1](https://tollbit.com/licensing-platform/)<br>[2](https://docs.tollbit.com/docs/monetization) | High / verify before seed | AI content licensing and publisher monetization infrastructure. |
| Trade Desk | [https://www.thetradedesk.com/](https://www.thetradedesk.com/) | [1](https://www.thetradedesk.com/us/solutions)<br>[2](https://www.thetradedesk.com/us/about-us/newsroom)<br>[3](https://www.thetradedesk.com/us/careers) | High / verify before seed | Independent DSP; monitor pharma/healthcare marketplace and BYOP integration signals. |
| UpToDate / Wolters Kluwer | [https://www.wolterskluwer.com/en/solutions/uptodate](https://www.wolterskluwer.com/en/solutions/uptodate) | [1](https://www.wolterskluwer.com/en/solutions/uptodate/about)<br>[2](https://www.uptodate.com/login) | High / verify before seed | Clinical knowledge destination, AI/clinical intelligence watchlist. |
| Veeva AI for Vault CRM | [https://www.veeva.com/products/crm-suite/veeva-ai-for-vault-crm/](https://www.veeva.com/products/crm-suite/veeva-ai-for-vault-crm/) | [1](https://www.veeva.com/products/crm-suite/veeva-ai-for-vault-crm/)<br>[2](https://www.veeva.com/products/crm-suite/)<br>[3](https://www.veeva.com/resources) | High / verify before seed | CRM incumbent; Vault CRM AI for life sciences commercial teams. |
| Veeva Crossix | [https://www.veeva.com/products/marketing-analytics/](https://www.veeva.com/products/marketing-analytics/) | [1](https://www.veeva.com/products/crossix-data-platform/)<br>[2](https://veevacrossix.com/)<br>[3](https://www.veeva.com/resources) | High / verify before seed | Marketing analytics, Crossix data platform, patient/HCP measurement. |
| Veradigm | [https://veradigm.com/](https://veradigm.com/) | [1](https://veradigm.com/about-veradigm/careers/join-our-team/)<br>[2](https://veradigm.com/news/)<br>[3](https://veradigm.com/solutions/) | High / verify before seed | EHR, Veradigm Network, Digital Health Media, data/analytics. |
| Vistar Media | [https://www.vistarmedia.com/](https://www.vistarmedia.com/) | [1](https://www.vistarmedia.com/news)<br>[2](https://www.vistarmedia.com/blog)<br>[3](https://www.vistarmedia.com/careers) | High / verify before seed | Programmatic DOOH marketplace/platform. |

---

## Master Product-to-Competitor Summary Matrix

| Product | High / Direct Competitors | Medium / Adjacent Competitors | Watchlist / Low Competitors |
|---|---|---|---|
| Marketplace | IQVIA, Definitive Healthcare, Komodo Health | DeepIntent, Doximity, IQVIA Digital, Medscape (WebMD Health), PulsePoint, StackAdapt, Swoop | CoverMyMeds, OptimizeRx, Veradigm, PatientPoint, Relevate Health, Trade Desk |
| Audience Quality Score | IQVIA, Komodo Health | Definitive Healthcare, Swoop, Veeva Crossix | None identified yet |
| ABM | None identified yet | IQVIA, 6sense, Definitive Healthcare, Demandbase | None identified yet |
| Premium Programmatic | DeepIntent, PulsePoint, StackAdapt, Swoop, Trade Desk | Doximity, IQVIA, IQVIA Digital, Medscape (WebMD Health), OptimizeRx, PatientPoint, Relevate Health | OpenEvidence, Veradigm, Komodo Health |
| Content Marketing | Doximity, Medscape / WebMD Health | Haymarket / M3 / Everyday Health Professional, IQVIA Digital, Outbrain, Taboola | None identified yet |
| RepTwin | RoseRx, Synthio Labs | Doximity, OpenEvidence, Hippocratic AI, Aktana / PharmaForceIQ, PrescriberPoint / Prescriber.AI, Salesforce Agentforce for Life Sciences, Veeva AI for Vault CRM | DeepIntent, IQVIA, Medscape (WebMD Health), OptimizeRx, PulsePoint, Swoop, Agilisium Pharma Rep Copilot, MathCo RepGPT, Openhelix |
| Point-of-Care | OptimizeRx, Veradigm, Relevate Health | ConnectiveRx, CoverMyMeds, DeepIntent, IQVIA, IQVIA Digital, PulsePoint, PatientPoint, Swoop | OpenEvidence, Komodo Health, StackAdapt |
| NEXT | DeepIntent, IQVIA, IQVIA Digital | OptimizeRx, PulsePoint, Veradigm, Komodo Health, Relevate Health, StackAdapt, Swoop, Trade Desk | CoverMyMeds, Doximity, Medscape (WebMD Health), OpenEvidence |
| Clinical Intent Signals | IQVIA, Komodo Health | DeepIntent, PulsePoint, Swoop, Veeva Crossix | None identified yet |
| co-pay.com | ConnectiveRx, CoverMyMeds | IQVIA, OptimizeRx, Veradigm, GoodRx, Relevate Health | DeepIntent, Komodo Health, RedSail Technologies |
| Point-of-Dispense | ConnectiveRx, RedSail Technologies | CoverMyMeds, OptimizeRx | IQVIA, GoodRx |
| Admanager | Google Ad Manager | AdButler, Kevel, PubMatic, Smaato | Magnite |
| Publisher AI Suite | Doximity, Medscape / WebMD Health, OpenEvidence | CCC, Dappier, TollBit, UpToDate / Wolters Kluwer | None identified yet |
| Spark for EHRs | OptimizeRx, Veradigm | PrescriberPoint, Relevate Health | DeepIntent |
| Spark for DOOH | CheckedUp, PatientPoint | DeepIntent via Place Exchange, Place Exchange, Screenverse, Vistar Media | None identified yet |
| Spark for Pharmacy | ConnectiveRx, RedSail Technologies / PioneerRx, RelayHealth / Change Healthcare / Optum Insight | CoverMyMeds, DrFirst, MedAdvisor, OptimizeRx | None identified yet |
| co-pay.com for Health Systems | ConnectiveRx, CoverMyMeds, OptimizeRx, Veradigm | AssistRx, PrescriberPoint, Relevate Health, Surescripts | None identified yet |

---

## Naming Correction: Lasso → IQVIA Digital

### Active Naming Rule

Use **IQVIA Digital** as the active competitor name in all new documentation, seed files, dashboards, reports, and battlecards.

### Legacy Aliases to Preserve

- Lasso
- Lasso Platform
- Lasso Marketing
- Lasso (an IQVIA business)
- IQVIA Lasso
- `lassoplatform.io` if historical pages or archive links appear

### Where IQVIA Digital Should Map

| Doceree Product | Overlap | Why |
|---|---:|---|
| NEXT | High | Omnichannel healthcare marketing, audience activation, measurement, campaign personalization, and IQVIA data leverage. |
| Premium Programmatic | Medium | Programmatic, endemic, social, email and CTV activation overlap. |
| Marketplace | Medium | Audience planning and activation overlap through IQVIA data and digital marketing workflows. |
| Point-of-Care | Medium | Workflow-adjacent healthcare activation; monitor for EHR/POC inventory or trigger language. |
| Clinical Intent Signals | Medium | Monitor if IQVIA Digital promotes real-time insights, advanced segmentation, personalization or intent-scoring. |
| ABM | Low / Medium | Escalate if account-level healthcare decision-maker targeting appears. |

---
## 1. Marketplace

**Journey / role:** Audience Matching
**Doceree product essence:** Custom HCP audience construction from verified clinical, behavioral, prescribing and EHR signals; activated inside Doceree or external DSPs.

### Competitive Frame

This is a demand-side product. The competitive frame should include direct product competitors, adjacent platform competitors, data/identity competitors, activation competitors, and category-shaping entrants that could influence buyer perception or budget allocation.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| IQVIA | [IQVIA](https://www.iqvia.com/) | [Official](https://www.iqvia.com/)<br>[Monitor 1](https://www.iqvia.com/newsroom)<br>[Monitor 2](https://www.iqvia.com/solutions)<br>[Monitor 3](https://iqvia.wd1.myworkdayjobs.com/IQVIA/) | High / direct | 1 | Healthcare data, analytics, technology | Data-scale dominance; agentic-AI direction; Lasso-Doceree NEXT head-to-head. | NPA, NSP, MIDAS, OneKey, E360 RWD |
| Definitive Healthcare | [Definitive Healthcare](https://www.definitivehc.com/) | [Official](https://www.definitivehc.com/)<br>[Monitor 1](https://www.definitivehc.com/solutions)<br>[Monitor 2](https://www.definitivehc.com/blog)<br>[Monitor 3](https://www.definitivehc.com/about/careers) | High / direct | 2 | Healthcare commercial intelligence | Marketplace data competitor. | View Suite, Monocl Expert, Carevoyance, Populi, APIs |
| Komodo Health | [Komodo Health](https://www.komodohealth.com/) | [Official](https://www.komodohealth.com/)<br>[Monitor 1](https://www.komodohealth.com/solutions)<br>[Monitor 2](https://www.komodohealth.com/insights)<br>[Monitor 3](https://www.komodohealth.com/careers/life-at-komodo/) | High / direct | 2 | Healthcare data; Real-World Data | Marketplace data competitor; Marmot AI threatens NEXT positioning. | Healthcare Map, MapLab, MapLab Enterprise, MapView, MapExplorer |
| DeepIntent | [DeepIntent](https://deepintent.com/) | [Official](https://deepintent.com/)<br>[Monitor 1](https://deepintent.com/news)<br>[Monitor 2](https://deepintent.com/careers)<br>[Monitor 3](https://deepintent.com/solutions) | Medium / adjacent | 1 | Healthcare DSP | Cortex repositioning as orchestration parity with NEXT; Helix infrastructure; Place Exchange DOOH reach. | DeepIntent DSP, DeepIntent Cortex, DeepIntent Helix, MarketMatch Planner, Audience Marketplace |
| Doximity | [Doximity](https://www.doximity.com/) | [Official](https://www.doximity.com/)<br>[Monitor 1](https://www.doximity.com/marketing-solutions)<br>[Monitor 2](https://press.doximity.com/)<br>[Monitor 3](https://www.doximity.com/careers) | Medium / adjacent | 1 | HCP destination network; HCP advertising | HCP audience destination; DocsGPT competes with Site-specific LLM. | Doximity platform, DocsGPT, Doximity GPT for clinicians, Physician job marketplace, Telehealth |
| IQVIA Digital | [IQVIA Digital](https://www.iqviadigital.com/) | [Official](https://www.iqviadigital.com/)<br>[Monitor 1](https://www.iqviadigital.com/solutions)<br>[Monitor 2](https://www.iqviadigital.com/resources)<br>[Monitor 3](https://www.iqviadigital.com/about-us/careers) | Medium / adjacent | 1 | Omnichannel healthcare marketing and analytics platform; legacy Lasso, now active as IQVIA Digital | Walled-garden alternative bundled with IQVIA data. | IQVIA Digital, legacy Lasso omnichannel healthcare marketing platform |
| Medscape (WebMD Health) | [Medscape (WebMD Health)](https://www.medscapeglobal.com/) | [Official](https://www.medscapeglobal.com/)<br>[Monitor 1](https://www.medscape.com/)<br>[Monitor 2](https://www.webmd.com/mediakit)<br>[Monitor 3](https://jobs.jobvite.com/webmd/jobs) | Medium / adjacent | 1 | HCP destination; CME; medical news | HCP destination; Authenticated NPI feeds PulsePoint. | Medscape platform, Medscape Extend, CME |
| PulsePoint | [PulsePoint](https://www.pulsepoint.com/) | [Official](https://www.pulsepoint.com/)<br>[Monitor 1](https://www.pulsepoint.com/resources/newsroom)<br>[Monitor 2](https://blog.pulsepoint.com/)<br>[Monitor 3](https://jobs.jobvite.com/pulsepoint/jobs) | Medium / adjacent | 1 | Healthcare programmatic; HCP measurement | Identity-layer competition via Medscape data; programmatic scale; HCP365 measurement. | PulsePoint platform, HCP365, Signal Platform, HCP Direct Match, HCP Explorer |
| StackAdapt | [StackAdapt](https://www.stackadapt.com/) | [Official](https://www.stackadapt.com/)<br>[Monitor 1](https://www.stackadapt.com/our-solutions/npi-targeting-and-measurement)<br>[Monitor 2](https://www.stackadapt.com/resources)<br>[Monitor 3](https://www.stackadapt.com/careers) | Medium / adjacent | 2 | AI-powered programmatic | Self-serve programmatic alternative for pharma agencies. | StackAdapt platform, Healthcare suite (NPI Targeting, Script Lift, EHR Inventory) |
| Swoop | [Swoop](https://swoop.com/) | [Official](https://swoop.com/)<br>[Monitor 1](https://swoop.com/)<br>[Monitor 2](https://ats.rippling.com/swoopishiring/jobs) | Medium / adjacent | 2 | Predictive HCP / patient audience platform | Predictive audience competition. | Swoop omnichannel marketing platform, Swoop Piper |
| CoverMyMeds | [CoverMyMeds](https://www.covermymeds.health/) | [Official](https://www.covermymeds.health/)<br>[Monitor 1](https://www.covermymeds.health/our-solutions)<br>[Monitor 2](https://www.covermymeds.health/about/newsroom)<br>[Monitor 3](https://talentcommunity.mckesson.com/flows/cmm) | Low / watchlist | 1 | Patient access; prior authorization; affordability | Workflow-incumbency; existing PA relationships difficult to displace. | PA platform, Benefits verification, Affordability and patient access products |
| OptimizeRx | [OptimizeRx](https://www.optimizerx.com/) | [Official](https://www.optimizerx.com/)<br>[Monitor 1](https://investors.optimizerx.com/news-releases)<br>[Monitor 2](https://www.optimizerx.com/blog)<br>[Monitor 3](https://www.optimizerx.com/careers) | Low / watchlist | 1 | Point-of-care marketing; healthcare omnichannel | Direct head-to-head loss source on POC; DAAP can be misread as orchestration parity with NEXT; pharmacy-adjacent moves overlap with POD. | DAAP, Micro-Neighborhood Targeting, EHR/ePrescribe placements, Patient-chart messaging |
| Veradigm | [Veradigm](https://veradigm.com/) | [Official](https://veradigm.com/)<br>[Monitor 1](https://veradigm.com/about-veradigm/careers/join-our-team/)<br>[Monitor 2](https://veradigm.com/news/)<br>[Monitor 3](https://veradigm.com/solutions/) | Low / watchlist | 1 | EHR ad media; healthcare data and provider-network tech | Strong incumbent on POC. | Veradigm Digital Health Media, Veradigm Network, Allscripts ambulatory EHRs |
| PatientPoint | [PatientPoint](https://patientpoint.com/) | [Official](https://patientpoint.com/)<br>[Monitor 1](https://careers.patientpoint.com/)<br>[Monitor 2](https://careers.patientpoint.com/search/searchjobs)<br>[Monitor 3](https://patientpoint.com/) | Low / watchlist | 2 | Owned point-of-care DOOH network | Owned network with programmatic capabilities competes with Spark for DOOH. | PatientPoint network, PatientPoint Health Audiences |
| Relevate Health | [Relevate Health](https://www.relevatehealth.com/) | [Official](https://www.relevatehealth.com/)<br>[Monitor 1](https://www.relevatehealth.com/news)<br>[Monitor 2](https://www.relevatehealth.com/blogs/enhancing-hcp-customer-experience-within-the-ehr-workflow)<br>[Monitor 3](https://www.relevatehealth.com/careers) | Low / watchlist | 2 | Pharma agency-tech hybrid | Direct POC competitor; agency-tech bundle attractive to brands looking for one vendor. | ELE Decision Engine, EHR-workflow-triggered messages, Level Ex pharma games |
| Trade Desk | [Trade Desk](https://www.thetradedesk.com/) | [Official](https://www.thetradedesk.com/)<br>[Monitor 1](https://www.thetradedesk.com/us/solutions)<br>[Monitor 2](https://www.thetradedesk.com/us/about-us/newsroom)<br>[Monitor 3](https://www.thetradedesk.com/us/careers) | Low / watchlist | 2 | Independent omnichannel DSP; pharma marketplace | Direct Premium Programmatic competitor; also a BYOP integration partner. | TTD DSP, Sellers and Publishers 500+, OpenPath, HCP endemic pharma marketplace |

### What to Monitor

- `custom audience builder`
- `HCP identity graph`
- `NPI match`
- `clinical signals`
- `EHR signals`
- `audience marketplace`
- `LiveRamp activation`
- `prescriber propensity`
- `treatment-line progression`
- `claims + EHR data`

### High-Signal Competitor Moves

- new custom HCP audience builder
- new real-time EHR/clinical data source
- new deterministic HCP identity graph
- audience activation into external DSPs
- prescriber propensity or treatment-window scoring
- LiveRamp/data clean room partnership

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent

---

## 2. Audience Quality Score

**Journey / role:** Cross-product audience prioritization
**Doceree product essence:** 0-100 HCP prescribing-likelihood scoring and budget-tiering layer.

### Competitive Frame

This is a demand-side product. The competitive frame should include direct product competitors, adjacent platform competitors, data/identity competitors, activation competitors, and category-shaping entrants that could influence buyer perception or budget allocation.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| IQVIA | [IQVIA](https://www.iqvia.com/) | [Official](https://www.iqvia.com/)<br>[Monitor 1](https://www.iqvia.com/newsroom)<br>[Monitor 2](https://www.iqvia.com/solutions)<br>[Monitor 3](https://iqvia.wd1.myworkdayjobs.com/IQVIA/) | High / direct | research | Direct data/analytics benchmark | Data/prediction vendor with large Rx/HCP datasets; AQS competes when buyers seek prescribing-likelihood scoring from incumbent data vendors. |  |
| Komodo Health | [Komodo Health](https://www.komodohealth.com/) | [Official](https://www.komodohealth.com/)<br>[Monitor 1](https://www.komodohealth.com/solutions)<br>[Monitor 2](https://www.komodohealth.com/insights)<br>[Monitor 3](https://www.komodohealth.com/careers/life-at-komodo/) | High / direct | research | Direct data/analytics benchmark | Healthcare Map and predictive/patient journey analytics can be used for audience prioritization and prescriber potential modeling. |  |
| Definitive Healthcare | [Definitive Healthcare](https://www.definitivehc.com/) | [Official](https://www.definitivehc.com/)<br>[Monitor 1](https://www.definitivehc.com/solutions)<br>[Monitor 2](https://www.definitivehc.com/blog)<br>[Monitor 3](https://www.definitivehc.com/about/careers) | Medium / adjacent | research | Adjacent intelligence benchmark | Provider/account intelligence and healthcare commercial intelligence can support list scoring and prioritization. |  |
| Swoop | [Swoop](https://swoop.com/) | [Official](https://swoop.com/)<br>[Monitor 1](https://swoop.com/)<br>[Monitor 2](https://ats.rippling.com/swoopishiring/jobs) | Medium / adjacent | research | Adjacent scoring + activation | Predictive patient/HCP audience platform; overlaps when scoring is tied to media activation. |  |
| Veeva Crossix | [Veeva Crossix](https://www.veeva.com/products/marketing-analytics/) | [Official](https://www.veeva.com/products/marketing-analytics/)<br>[Monitor 1](https://www.veeva.com/products/crossix-data-platform/)<br>[Monitor 2](https://veevacrossix.com/)<br>[Monitor 3](https://www.veeva.com/resources) | Medium / adjacent | research | Measurement-adjacent | Measurement and analytics layer adjacent to audience quality, targeting, and Rx impact. |  |

### What to Monitor

- `audience quality`
- `propensity score`
- `prescribing likelihood`
- `HCP scoring`
- `prescriber readiness`
- `list quality`
- `potential prescribers`
- `predictive audience`
- `budget tiering`

### High-Signal Competitor Moves

- new prescribing likelihood score
- validated HCP propensity model
- audience quality benchmark
- budget allocation guidance by HCP tier
- potential prescriber model
- case study showing lift from scored HCP tiers

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent

---

## 3. ABM

**Journey / role:** Account Influence
**Doceree product essence:** Healthcare-native account-based marketing across hospitals, IDNs, academic centers, specialty pharmacies and clinics.

### Competitive Frame

This is a demand-side product. The competitive frame should include direct product competitors, adjacent platform competitors, data/identity competitors, activation competitors, and category-shaping entrants that could influence buyer perception or budget allocation.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| IQVIA | [IQVIA](https://www.iqvia.com/) | [Official](https://www.iqvia.com/)<br>[Monitor 1](https://www.iqvia.com/newsroom)<br>[Monitor 2](https://www.iqvia.com/solutions)<br>[Monitor 3](https://iqvia.wd1.myworkdayjobs.com/IQVIA/) | Medium / adjacent | 1 | Healthcare data, analytics, technology | Data-scale dominance; agentic-AI direction; Lasso-Doceree NEXT head-to-head. | NPA, NSP, MIDAS, OneKey, E360 RWD |
| 6sense | [6sense](https://6sense.com/) | [Official](https://6sense.com/)<br>[Monitor 1](https://6sense.com/newsroom/)<br>[Monitor 2](https://6sense.com/product/)<br>[Monitor 3](https://6sense.com/careers/) | Medium / adjacent | 2 | Generic B2B ABM with AI | AI agent direction overlaps RepTwin if extended to healthcare. | 6sense Revenue AI, AI agents for GTM tasks |
| Definitive Healthcare | [Definitive Healthcare](https://www.definitivehc.com/) | [Official](https://www.definitivehc.com/)<br>[Monitor 1](https://www.definitivehc.com/solutions)<br>[Monitor 2](https://www.definitivehc.com/blog)<br>[Monitor 3](https://www.definitivehc.com/about/careers) | Medium / adjacent | 2 | Healthcare commercial intelligence | Marketplace data competitor. | View Suite, Monocl Expert, Carevoyance, Populi, APIs |
| Demandbase | [Demandbase](https://www.demandbase.com/) | [Official](https://www.demandbase.com/)<br>[Monitor 1](https://www.demandbase.com/products/account-based-experience/)<br>[Monitor 2](https://www.demandbase.com/about-us/news/)<br>[Monitor 3](https://www.demandbase.com/careers/) | Medium / adjacent | 2 | Generic B2B ABM | If launches a healthcare module, threat escalates. | Demandbase One |

### What to Monitor

- `healthcare ABM`
- `IDN targeting`
- `account lift`
- `P&T committee`
- `value analysis committee`
- `hospital targeting`
- `firmographics`
- `intent data`
- `IP targeting`
- `role-based account targeting`

### High-Signal Competitor Moves

- healthcare-specific ABM module
- IDN/hospital account-targeting product
- P&T/VAC stakeholder mapping
- account lift proof point
- medical publisher or healthcare-intent partnership
- healthcare compliance module added by generic ABM player

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent

---

## 4. Premium Programmatic

**Journey / role:** Awareness
**Doceree product essence:** Verified-HCP endemic programmatic media across specialist medical publishers using NPI + medical context.

### Competitive Frame

This is a demand-side product. The competitive frame should include direct product competitors, adjacent platform competitors, data/identity competitors, activation competitors, and category-shaping entrants that could influence buyer perception or budget allocation.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| DeepIntent | [DeepIntent](https://deepintent.com/) | [Official](https://deepintent.com/)<br>[Monitor 1](https://deepintent.com/news)<br>[Monitor 2](https://deepintent.com/careers)<br>[Monitor 3](https://deepintent.com/solutions) | High / direct | 1 | Healthcare DSP | Cortex repositioning as orchestration parity with NEXT; Helix infrastructure; Place Exchange DOOH reach. | DeepIntent DSP, DeepIntent Cortex, DeepIntent Helix, MarketMatch Planner, Audience Marketplace |
| PulsePoint | [PulsePoint](https://www.pulsepoint.com/) | [Official](https://www.pulsepoint.com/)<br>[Monitor 1](https://www.pulsepoint.com/resources/newsroom)<br>[Monitor 2](https://blog.pulsepoint.com/)<br>[Monitor 3](https://jobs.jobvite.com/pulsepoint/jobs) | High / direct | 1 | Healthcare programmatic; HCP measurement | Identity-layer competition via Medscape data; programmatic scale; HCP365 measurement. | PulsePoint platform, HCP365, Signal Platform, HCP Direct Match, HCP Explorer |
| StackAdapt | [StackAdapt](https://www.stackadapt.com/) | [Official](https://www.stackadapt.com/)<br>[Monitor 1](https://www.stackadapt.com/our-solutions/npi-targeting-and-measurement)<br>[Monitor 2](https://www.stackadapt.com/resources)<br>[Monitor 3](https://www.stackadapt.com/careers) | High / direct | 2 | AI-powered programmatic | Self-serve programmatic alternative for pharma agencies. | StackAdapt platform, Healthcare suite (NPI Targeting, Script Lift, EHR Inventory) |
| Swoop | [Swoop](https://swoop.com/) | [Official](https://swoop.com/)<br>[Monitor 1](https://swoop.com/)<br>[Monitor 2](https://ats.rippling.com/swoopishiring/jobs) | High / direct | 2 | Predictive HCP / patient audience platform | Predictive audience competition. | Swoop omnichannel marketing platform, Swoop Piper |
| Trade Desk | [Trade Desk](https://www.thetradedesk.com/) | [Official](https://www.thetradedesk.com/)<br>[Monitor 1](https://www.thetradedesk.com/us/solutions)<br>[Monitor 2](https://www.thetradedesk.com/us/about-us/newsroom)<br>[Monitor 3](https://www.thetradedesk.com/us/careers) | High / direct | 2 | Independent omnichannel DSP; pharma marketplace | Direct Premium Programmatic competitor; also a BYOP integration partner. | TTD DSP, Sellers and Publishers 500+, OpenPath, HCP endemic pharma marketplace |
| Doximity | [Doximity](https://www.doximity.com/) | [Official](https://www.doximity.com/)<br>[Monitor 1](https://www.doximity.com/marketing-solutions)<br>[Monitor 2](https://press.doximity.com/)<br>[Monitor 3](https://www.doximity.com/careers) | Medium / adjacent | 1 | HCP destination network; HCP advertising | HCP audience destination; DocsGPT competes with Site-specific LLM. | Doximity platform, DocsGPT, Doximity GPT for clinicians, Physician job marketplace, Telehealth |
| IQVIA | [IQVIA](https://www.iqvia.com/) | [Official](https://www.iqvia.com/)<br>[Monitor 1](https://www.iqvia.com/newsroom)<br>[Monitor 2](https://www.iqvia.com/solutions)<br>[Monitor 3](https://iqvia.wd1.myworkdayjobs.com/IQVIA/) | Medium / adjacent | 1 | Healthcare data, analytics, technology | Data-scale dominance; agentic-AI direction; Lasso-Doceree NEXT head-to-head. | NPA, NSP, MIDAS, OneKey, E360 RWD |
| IQVIA Digital | [IQVIA Digital](https://www.iqviadigital.com/) | [Official](https://www.iqviadigital.com/)<br>[Monitor 1](https://www.iqviadigital.com/solutions)<br>[Monitor 2](https://www.iqviadigital.com/resources)<br>[Monitor 3](https://www.iqviadigital.com/about-us/careers) | Medium / adjacent | 1 | Omnichannel healthcare marketing and analytics platform; legacy Lasso, now active as IQVIA Digital | Walled-garden alternative bundled with IQVIA data. | IQVIA Digital, legacy Lasso omnichannel healthcare marketing platform |
| Medscape (WebMD Health) | [Medscape (WebMD Health)](https://www.medscapeglobal.com/) | [Official](https://www.medscapeglobal.com/)<br>[Monitor 1](https://www.medscape.com/)<br>[Monitor 2](https://www.webmd.com/mediakit)<br>[Monitor 3](https://jobs.jobvite.com/webmd/jobs) | Medium / adjacent | 1 | HCP destination; CME; medical news | HCP destination; Authenticated NPI feeds PulsePoint. | Medscape platform, Medscape Extend, CME |
| OptimizeRx | [OptimizeRx](https://www.optimizerx.com/) | [Official](https://www.optimizerx.com/)<br>[Monitor 1](https://investors.optimizerx.com/news-releases)<br>[Monitor 2](https://www.optimizerx.com/blog)<br>[Monitor 3](https://www.optimizerx.com/careers) | Medium / adjacent | 1 | Point-of-care marketing; healthcare omnichannel | Direct head-to-head loss source on POC; DAAP can be misread as orchestration parity with NEXT; pharmacy-adjacent moves overlap with POD. | DAAP, Micro-Neighborhood Targeting, EHR/ePrescribe placements, Patient-chart messaging |
| PatientPoint | [PatientPoint](https://patientpoint.com/) | [Official](https://patientpoint.com/)<br>[Monitor 1](https://careers.patientpoint.com/)<br>[Monitor 2](https://careers.patientpoint.com/search/searchjobs)<br>[Monitor 3](https://patientpoint.com/) | Medium / adjacent | 2 | Owned point-of-care DOOH network | Owned network with programmatic capabilities competes with Spark for DOOH. | PatientPoint network, PatientPoint Health Audiences |
| Relevate Health | [Relevate Health](https://www.relevatehealth.com/) | [Official](https://www.relevatehealth.com/)<br>[Monitor 1](https://www.relevatehealth.com/news)<br>[Monitor 2](https://www.relevatehealth.com/blogs/enhancing-hcp-customer-experience-within-the-ehr-workflow)<br>[Monitor 3](https://www.relevatehealth.com/careers) | Medium / adjacent | 2 | Pharma agency-tech hybrid | Direct POC competitor; agency-tech bundle attractive to brands looking for one vendor. | ELE Decision Engine, EHR-workflow-triggered messages, Level Ex pharma games |
| OpenEvidence | [OpenEvidence](https://www.openevidence.com/) | [Official](https://www.openevidence.com/)<br>[Monitor 1](https://www.openevidence.com/) | Low / watchlist | 1 | Clinical AI for physicians | Diverts HCP attention from Doceree publisher network; absorbs AI-era query volume. | OpenEvidence platform, OpenEvidence DeepConsult |
| Veradigm | [Veradigm](https://veradigm.com/) | [Official](https://veradigm.com/)<br>[Monitor 1](https://veradigm.com/about-veradigm/careers/join-our-team/)<br>[Monitor 2](https://veradigm.com/news/)<br>[Monitor 3](https://veradigm.com/solutions/) | Low / watchlist | 1 | EHR ad media; healthcare data and provider-network tech | Strong incumbent on POC. | Veradigm Digital Health Media, Veradigm Network, Allscripts ambulatory EHRs |
| Komodo Health | [Komodo Health](https://www.komodohealth.com/) | [Official](https://www.komodohealth.com/)<br>[Monitor 1](https://www.komodohealth.com/solutions)<br>[Monitor 2](https://www.komodohealth.com/insights)<br>[Monitor 3](https://www.komodohealth.com/careers/life-at-komodo/) | Low / watchlist | 2 | Healthcare data; Real-World Data | Marketplace data competitor; Marmot AI threatens NEXT positioning. | Healthcare Map, MapLab, MapLab Enterprise, MapView, MapExplorer |

### What to Monitor

- `healthcare DSP`
- `HCP programmatic`
- `endemic publishers`
- `NPI-level targeting`
- `contextual targeting`
- `MeSH taxonomy`
- `HCP365`
- `verified HCP`
- `keyword-level reporting`
- `creative analytics`

### High-Signal Competitor Moves

- new HCP DSP feature
- medical publisher network expansion
- NPI-level identity improvement
- contextual medical taxonomy launch
- keyword-level reporting
- AI media buying / optimization
- new endemic inventory partnership

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent, Partnership / Integration Agent, Case Study / Proof Point Agent, SEO / Category Narrative Agent (approved source pages only)

---

## 5. Content Marketing

**Journey / role:** Awareness / Education
**Doceree product essence:** Long-form scientific content distribution across the endemic publisher network and related supply-side publisher surfaces.

### Competitive Frame

This is a demand-side product. The competitive frame should include direct product competitors, adjacent platform competitors, data/identity competitors, activation competitors, and category-shaping entrants that could influence buyer perception or budget allocation.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| Doximity | [Doximity](https://www.doximity.com/) | [Official](https://www.doximity.com/)<br>[Monitor 1](https://www.doximity.com/marketing-solutions)<br>[Monitor 2](https://press.doximity.com/)<br>[Monitor 3](https://www.doximity.com/careers) | High / direct | research | Direct endemic HCP network competitor | Physician network/content destination with sponsored education and HCP engagement surfaces. |  |
| Medscape / WebMD Health | [Medscape / WebMD Health](https://www.medscapeglobal.com/) | [Official](https://www.medscapeglobal.com/)<br>[Monitor 1](https://www.medscape.com/)<br>[Monitor 2](https://www.webmd.com/mediakit)<br>[Monitor 3](https://jobs.jobvite.com/webmd/jobs) | High / direct | research | Direct endemic content competitor | Endemic HCP content destination and publisher network; competes for sponsored medical education and content distribution budgets. |  |
| Haymarket / M3 / Everyday Health Professional | [Haymarket / M3 / Everyday Health Professional](https://www.haymarketmedia.com/) | [Official](https://www.haymarketmedia.com/)<br>[Monitor 1](https://corporate.m3.com/)<br>[Monitor 2](https://www.everydayhealthgroup.com/)<br>[Monitor 3](https://www.haymarketmedicalnetwork.com/) | Medium / adjacent | research | Publisher/content competitor | Medical publisher/content networks that compete for HCP educational-content sponsorship. |  |
| IQVIA Digital | [IQVIA Digital](https://www.iqviadigital.com/) | [Official](https://www.iqviadigital.com/)<br>[Monitor 1](https://www.iqviadigital.com/solutions)<br>[Monitor 2](https://www.iqviadigital.com/resources)<br>[Monitor 3](https://www.iqviadigital.com/about-us/careers) | Medium / adjacent | research | Omnichannel content activation | Omnichannel healthcare activation can compete when content is distributed through healthcare marketing workflows. |  |
| Outbrain | [Outbrain](https://www.outbrain.com/) | [Official](https://www.outbrain.com/)<br>[Monitor 1](https://www.outbrain.com/advertisers/)<br>[Monitor 2](https://www.outbrain.com/blog/)<br>[Monitor 3](https://www.outbrain.com/careers/) | Medium / adjacent | research | Generic syndication benchmark | Generic content-discovery/syndication alternative; weaker because not healthcare-native. |  |
| Taboola | [Taboola](https://www.taboola.com/) | [Official](https://www.taboola.com/)<br>[Monitor 1](https://www.taboola.com/advertisers)<br>[Monitor 2](https://www.taboola.com/resources)<br>[Monitor 3](https://www.taboola.com/careers) | Medium / adjacent | research | Generic syndication benchmark | Generic content-discovery/syndication alternative; weaker because not healthcare-native. |  |

### What to Monitor

- `scientific content distribution`
- `sponsored medical education`
- `content syndication`
- `publisher amplification`
- `native medical content`
- `HCP education`
- `medical publisher content`

### High-Signal Competitor Moves

- new scientific content distribution product
- medical publisher content network expansion
- sponsored content education product
- native content amplification
- brand content hub or MLR-grounded content assistant

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent, Partnership / Integration Agent, Case Study / Proof Point Agent, SEO / Category Narrative Agent (approved source pages only)

---

## 6. RepTwin

**Journey / role:** Interaction
**Doceree product essence:** MLR-trained multimodal AI virtual brand rep for HCP engagement, available across video, voice and chat.

### Competitive Frame

RepTwin competes in a fast-forming category: compliant AI agents for pharma, life sciences customer engagement, HCP conversations, patient support, field-force productivity, and medical-information delivery. The category should not be limited to companies that use the phrase “virtual rep.” Monitor any vendor building regulated life-sciences conversational agents, MLR-grounded AI engagement, HCP voice agents, patient-support agents, or CRM-native field agents.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| RoseRx | [RoseRx](https://www.roserx.ai/) | [Official](https://www.roserx.ai/)<br>[Monitor 1](https://www.roserx.ai/hcp-engagement-platform)<br>[Monitor 2](https://www.roserx.ai/about)<br>[Monitor 3](https://www.roserx.ai/contact) | High / direct | research | Direct pharma conversational-AI competitor | Conversational AI for pharma HCP and patient engagement using approved/MLR content, audit trails, omnichannel intelligence and compliance review. | official site |
| Synthio Labs | [Synthio Labs](https://synthiolabs.com/) | [Official](https://synthiolabs.com/)<br>[Monitor 1](https://synthiolabs.com/) | High / direct | research | Direct life-sciences agentic AI competitor | Multimodal agentic AI platform purpose-built for pharma workflows; includes Jarvis for field teams, Ather for HCP engagement, Helix for patient support, Simulation Studio and Polaris HQ. | official site; YC profile; BusinessWire funding |
| Doximity | [Doximity](https://www.doximity.com/) | [Official](https://www.doximity.com/)<br>[Monitor 1](https://www.doximity.com/marketing-solutions)<br>[Monitor 2](https://press.doximity.com/)<br>[Monitor 3](https://www.doximity.com/careers) | Medium / adjacent | 1 | HCP destination network; HCP advertising | HCP audience destination; DocsGPT competes with Site-specific LLM. | Doximity platform, DocsGPT, Doximity GPT for clinicians, Physician job marketplace, Telehealth |
| OpenEvidence | [OpenEvidence](https://www.openevidence.com/) | [Official](https://www.openevidence.com/)<br>[Monitor 1](https://www.openevidence.com/) | Medium / adjacent | 1 | Clinical AI for physicians | Diverts HCP attention from Doceree publisher network; absorbs AI-era query volume. | OpenEvidence platform, OpenEvidence DeepConsult |
| Hippocratic AI | [Hippocratic AI](https://hippocraticai.com/) | [Official](https://hippocraticai.com/)<br>[Monitor 1](https://hippocraticai.com/lifesciences/)<br>[Monitor 2](https://hippocraticai.com/healthcare-agents/)<br>[Monitor 3](https://hippocraticai.com/view-all-agents/) | Medium / adjacent | 2 | Healthcare AI agents (patient-care use cases) | Adjacent agentic AI — pharma rep replacement extension would directly threaten RepTwin. | Constellation Architecture multi-LLM safety framework, Patient-facing AI agents |
| Aktana / PharmaForceIQ | [Aktana / PharmaForceIQ](https://pharmaforceiq.com/) | [Official](https://pharmaforceiq.com/)<br>[Monitor 1](https://www.aktana.com/)<br>[Monitor 2](https://pharmaforceiq.com/pharmaforceiq-acquires-aktana/) | Medium / adjacent | research | NBA/orchestration competitor | AI-driven insights, orchestration and decision support for commercial/medical teams; acquired by PharmaForceIQ to create optichannel GTM tech. | official Aktana; PharmaForceIQ news |
| PrescriberPoint / Prescriber.AI | [PrescriberPoint / Prescriber.AI](https://prescriberpoint.com/) | [Official](https://prescriberpoint.com/)<br>[Monitor 1](https://prescriberpoint.com/prescriber-ai)<br>[Monitor 2](https://prescriberpoint.com/insights/introducing-prescriberai) | Medium / adjacent | research | POC + HCP assistant adjacent | AI-powered point-of-care platform for researching FDA-approved drug/clinical info, understanding coverage/OOP costs, PA, savings enrollment and brand activation. | official business site; press release |
| Salesforce Agentforce for Life Sciences | [Salesforce Agentforce for Life Sciences](https://www.salesforce.com/life-sciences/artificial-intelligence/) | [Official](https://www.salesforce.com/life-sciences/artificial-intelligence/)<br>[Monitor 1](https://www.salesforce.com/life-sciences/artificial-intelligence/)<br>[Monitor 2](https://www.salesforce.com/news/)<br>[Monitor 3](https://www.salesforce.com/products/agentforce/) | Medium / adjacent | research | Enterprise platform competitor | Agentic AI platform for pharma and medtech commercial, clinical and medical engagement at scale; strong platform risk because of CRM footprint. | official Salesforce |
| Veeva AI for Vault CRM | [Veeva AI for Vault CRM](https://www.veeva.com/products/crm-suite/veeva-ai-for-vault-crm/) | [Official](https://www.veeva.com/products/crm-suite/veeva-ai-for-vault-crm/)<br>[Monitor 1](https://www.veeva.com/products/crm-suite/veeva-ai-for-vault-crm/)<br>[Monitor 2](https://www.veeva.com/products/crm-suite/)<br>[Monitor 3](https://www.veeva.com/resources) | Medium / adjacent | research | CRM/field workflow AI competitor | Industry-specific AI embedded in Vault CRM; pre-call/voice/field workflow agents strengthen incumbent CRM position. | official Veeva |
| DeepIntent | [DeepIntent](https://deepintent.com/) | [Official](https://deepintent.com/)<br>[Monitor 1](https://deepintent.com/news)<br>[Monitor 2](https://deepintent.com/careers)<br>[Monitor 3](https://deepintent.com/solutions) | Low / watchlist | 1 | Healthcare DSP | Cortex repositioning as orchestration parity with NEXT; Helix infrastructure; Place Exchange DOOH reach. | DeepIntent DSP, DeepIntent Cortex, DeepIntent Helix, MarketMatch Planner, Audience Marketplace |
| IQVIA | [IQVIA](https://www.iqvia.com/) | [Official](https://www.iqvia.com/)<br>[Monitor 1](https://www.iqvia.com/newsroom)<br>[Monitor 2](https://www.iqvia.com/solutions)<br>[Monitor 3](https://iqvia.wd1.myworkdayjobs.com/IQVIA/) | Low / watchlist | 1 | Healthcare data, analytics, technology | Data-scale dominance; agentic-AI direction; Lasso-Doceree NEXT head-to-head. | NPA, NSP, MIDAS, OneKey, E360 RWD |
| Medscape (WebMD Health) | [Medscape (WebMD Health)](https://www.medscapeglobal.com/) | [Official](https://www.medscapeglobal.com/)<br>[Monitor 1](https://www.medscape.com/)<br>[Monitor 2](https://www.webmd.com/mediakit)<br>[Monitor 3](https://jobs.jobvite.com/webmd/jobs) | Low / watchlist | 1 | HCP destination; CME; medical news | HCP destination; Authenticated NPI feeds PulsePoint. | Medscape platform, Medscape Extend, CME |
| OptimizeRx | [OptimizeRx](https://www.optimizerx.com/) | [Official](https://www.optimizerx.com/)<br>[Monitor 1](https://investors.optimizerx.com/news-releases)<br>[Monitor 2](https://www.optimizerx.com/blog)<br>[Monitor 3](https://www.optimizerx.com/careers) | Low / watchlist | 1 | Point-of-care marketing; healthcare omnichannel | Direct head-to-head loss source on POC; DAAP can be misread as orchestration parity with NEXT; pharmacy-adjacent moves overlap with POD. | DAAP, Micro-Neighborhood Targeting, EHR/ePrescribe placements, Patient-chart messaging |
| PulsePoint | [PulsePoint](https://www.pulsepoint.com/) | [Official](https://www.pulsepoint.com/)<br>[Monitor 1](https://www.pulsepoint.com/resources/newsroom)<br>[Monitor 2](https://blog.pulsepoint.com/)<br>[Monitor 3](https://jobs.jobvite.com/pulsepoint/jobs) | Low / watchlist | 1 | Healthcare programmatic; HCP measurement | Identity-layer competition via Medscape data; programmatic scale; HCP365 measurement. | PulsePoint platform, HCP365, Signal Platform, HCP Direct Match, HCP Explorer |
| Swoop | [Swoop](https://swoop.com/) | [Official](https://swoop.com/)<br>[Monitor 1](https://swoop.com/)<br>[Monitor 2](https://ats.rippling.com/swoopishiring/jobs) | Low / watchlist | 2 | Predictive HCP / patient audience platform | Predictive audience competition. | Swoop omnichannel marketing platform, Swoop Piper |
| Agilisium Pharma Rep Copilot | [Agilisium Pharma Rep Copilot](https://www.agilisium.com/blogs/beyond-traditional-sales-how-ai-agents-are-transforming-hcp-engagement-in-life-sciences) | [Official](https://www.agilisium.com/blogs/beyond-traditional-sales-how-ai-agents-are-transforming-hcp-engagement-in-life-sciences)<br>[Monitor 1](https://www.agilisium.com/blogs/beyond-traditional-sales-how-ai-agents-are-transforming-hcp-engagement-in-life-sciences)<br>[Monitor 2](https://www.agilisium.com/) | Low / watchlist | research | Services/productized copilot | AI agent / copilot concept for HCP engagement and pharma sales workflows. | Agilisium blog |
| MathCo RepGPT | [MathCo RepGPT](https://mathco.com/article/sales-rep-assistant-repgpt-intelligent-multi-agent-ai-for-pharma-sales-built-on-databricks/) | [Official](https://mathco.com/article/sales-rep-assistant-repgpt-intelligent-multi-agent-ai-for-pharma-sales-built-on-databricks/)<br>[Monitor 1](https://mathco.com/article/sales-rep-assistant-repgpt-intelligent-multi-agent-ai-for-pharma-sales-built-on-databricks/)<br>[Monitor 2](https://mathco.com/) | Low / watchlist | research | Services/productized agent framework | Multi-agent AI framework for pharma sales representatives/MSLs; often services-led but should be monitored for productization. | MathCo case/article |
| Openhelix | [Openhelix](https://www.openhelix.co/) | [Official](https://www.openhelix.co/)<br>[Monitor 1](https://www.openhelix.co/) | Low / watchlist | research | Field-force copilot competitor | AI copilot for life-science reps and managers focused on rep productivity, admin burden, targeting and in-field time. | official site |

### What to Monitor

- `AI brand rep`
- `virtual rep`
- `agentic AI for pharma`
- `HCP voice agent`
- `medical information agent`
- `MLR-approved conversational AI`
- `AI digital rep`
- `field team copilot`
- `MSL AI`
- `FRM AI`
- `patient engagement agent`

### High-Signal Competitor Moves

- AI brand rep launch
- voice/chat/video HCP agent
- MLR-approved conversational AI
- AI medical-information agent
- field-team copilot
- MSL/FRM AI agent
- patient support agent expansion into pharma commercial
- CRM-native agent for HCP engagement

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent, Approved Social Intelligence Agent (approved sources only), Analyst / Market Report Agent (manual uploads only), Category Narrative Classifier

---

## 7. Point-of-Care

**Journey / role:** Clinical Decision
**Doceree product essence:** EHR workflow-native clinical-trigger messaging at the prescribing moment.

### Competitive Frame

This is a demand-side product. The competitive frame should include direct product competitors, adjacent platform competitors, data/identity competitors, activation competitors, and category-shaping entrants that could influence buyer perception or budget allocation.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| OptimizeRx | [OptimizeRx](https://www.optimizerx.com/) | [Official](https://www.optimizerx.com/)<br>[Monitor 1](https://investors.optimizerx.com/news-releases)<br>[Monitor 2](https://www.optimizerx.com/blog)<br>[Monitor 3](https://www.optimizerx.com/careers) | High / direct | 1 | Point-of-care marketing; healthcare omnichannel | Direct head-to-head loss source on POC; DAAP can be misread as orchestration parity with NEXT; pharmacy-adjacent moves overlap with POD. | DAAP, Micro-Neighborhood Targeting, EHR/ePrescribe placements, Patient-chart messaging |
| Veradigm | [Veradigm](https://veradigm.com/) | [Official](https://veradigm.com/)<br>[Monitor 1](https://veradigm.com/about-veradigm/careers/join-our-team/)<br>[Monitor 2](https://veradigm.com/news/)<br>[Monitor 3](https://veradigm.com/solutions/) | High / direct | 1 | EHR ad media; healthcare data and provider-network tech | Strong incumbent on POC. | Veradigm Digital Health Media, Veradigm Network, Allscripts ambulatory EHRs |
| Relevate Health | [Relevate Health](https://www.relevatehealth.com/) | [Official](https://www.relevatehealth.com/)<br>[Monitor 1](https://www.relevatehealth.com/news)<br>[Monitor 2](https://www.relevatehealth.com/blogs/enhancing-hcp-customer-experience-within-the-ehr-workflow)<br>[Monitor 3](https://www.relevatehealth.com/careers) | High / direct | 2 | Pharma agency-tech hybrid | Direct POC competitor; agency-tech bundle attractive to brands looking for one vendor. | ELE Decision Engine, EHR-workflow-triggered messages, Level Ex pharma games |
| ConnectiveRx | [ConnectiveRx](https://www.connectiverx.com/) | [Official](https://www.connectiverx.com/)<br>[Monitor 1](https://www.connectiverx.com/)<br>[Monitor 2](https://www.connectiverx.com/careers)<br>[Monitor 3](https://careers-connectiverx.icims.com/jobs/intro?mobile=true&needsRedirect=false) | Medium / adjacent | 1 | Patient affordability; co-pay coupons; hub services | Coupon-network incumbency. | Co-pay assistance, Coupon products, Clinically-integrated provider engagement network, Hub services |
| CoverMyMeds | [CoverMyMeds](https://www.covermymeds.health/) | [Official](https://www.covermymeds.health/)<br>[Monitor 1](https://www.covermymeds.health/our-solutions)<br>[Monitor 2](https://www.covermymeds.health/about/newsroom)<br>[Monitor 3](https://talentcommunity.mckesson.com/flows/cmm) | Medium / adjacent | 1 | Patient access; prior authorization; affordability | Workflow-incumbency; existing PA relationships difficult to displace. | PA platform, Benefits verification, Affordability and patient access products |
| DeepIntent | [DeepIntent](https://deepintent.com/) | [Official](https://deepintent.com/)<br>[Monitor 1](https://deepintent.com/news)<br>[Monitor 2](https://deepintent.com/careers)<br>[Monitor 3](https://deepintent.com/solutions) | Medium / adjacent | 1 | Healthcare DSP | Cortex repositioning as orchestration parity with NEXT; Helix infrastructure; Place Exchange DOOH reach. | DeepIntent DSP, DeepIntent Cortex, DeepIntent Helix, MarketMatch Planner, Audience Marketplace |
| IQVIA | [IQVIA](https://www.iqvia.com/) | [Official](https://www.iqvia.com/)<br>[Monitor 1](https://www.iqvia.com/newsroom)<br>[Monitor 2](https://www.iqvia.com/solutions)<br>[Monitor 3](https://iqvia.wd1.myworkdayjobs.com/IQVIA/) | Medium / adjacent | 1 | Healthcare data, analytics, technology | Data-scale dominance; agentic-AI direction; Lasso-Doceree NEXT head-to-head. | NPA, NSP, MIDAS, OneKey, E360 RWD |
| IQVIA Digital | [IQVIA Digital](https://www.iqviadigital.com/) | [Official](https://www.iqviadigital.com/)<br>[Monitor 1](https://www.iqviadigital.com/solutions)<br>[Monitor 2](https://www.iqviadigital.com/resources)<br>[Monitor 3](https://www.iqviadigital.com/about-us/careers) | Medium / adjacent | 1 | Omnichannel healthcare marketing and analytics platform; legacy Lasso, now active as IQVIA Digital | Walled-garden alternative bundled with IQVIA data. | IQVIA Digital, legacy Lasso omnichannel healthcare marketing platform |
| PulsePoint | [PulsePoint](https://www.pulsepoint.com/) | [Official](https://www.pulsepoint.com/)<br>[Monitor 1](https://www.pulsepoint.com/resources/newsroom)<br>[Monitor 2](https://blog.pulsepoint.com/)<br>[Monitor 3](https://jobs.jobvite.com/pulsepoint/jobs) | Medium / adjacent | 1 | Healthcare programmatic; HCP measurement | Identity-layer competition via Medscape data; programmatic scale; HCP365 measurement. | PulsePoint platform, HCP365, Signal Platform, HCP Direct Match, HCP Explorer |
| PatientPoint | [PatientPoint](https://patientpoint.com/) | [Official](https://patientpoint.com/)<br>[Monitor 1](https://careers.patientpoint.com/)<br>[Monitor 2](https://careers.patientpoint.com/search/searchjobs)<br>[Monitor 3](https://patientpoint.com/) | Medium / adjacent | 2 | Owned point-of-care DOOH network | Owned network with programmatic capabilities competes with Spark for DOOH. | PatientPoint network, PatientPoint Health Audiences |
| Swoop | [Swoop](https://swoop.com/) | [Official](https://swoop.com/)<br>[Monitor 1](https://swoop.com/)<br>[Monitor 2](https://ats.rippling.com/swoopishiring/jobs) | Medium / adjacent | 2 | Predictive HCP / patient audience platform | Predictive audience competition. | Swoop omnichannel marketing platform, Swoop Piper |
| OpenEvidence | [OpenEvidence](https://www.openevidence.com/) | [Official](https://www.openevidence.com/)<br>[Monitor 1](https://www.openevidence.com/) | Low / watchlist | 1 | Clinical AI for physicians | Diverts HCP attention from Doceree publisher network; absorbs AI-era query volume. | OpenEvidence platform, OpenEvidence DeepConsult |
| Komodo Health | [Komodo Health](https://www.komodohealth.com/) | [Official](https://www.komodohealth.com/)<br>[Monitor 1](https://www.komodohealth.com/solutions)<br>[Monitor 2](https://www.komodohealth.com/insights)<br>[Monitor 3](https://www.komodohealth.com/careers/life-at-komodo/) | Low / watchlist | 2 | Healthcare data; Real-World Data | Marketplace data competitor; Marmot AI threatens NEXT positioning. | Healthcare Map, MapLab, MapLab Enterprise, MapView, MapExplorer |
| StackAdapt | [StackAdapt](https://www.stackadapt.com/) | [Official](https://www.stackadapt.com/)<br>[Monitor 1](https://www.stackadapt.com/our-solutions/npi-targeting-and-measurement)<br>[Monitor 2](https://www.stackadapt.com/resources)<br>[Monitor 3](https://www.stackadapt.com/careers) | Low / watchlist | 2 | AI-powered programmatic | Self-serve programmatic alternative for pharma agencies. | StackAdapt platform, Healthcare suite (NPI Targeting, Script Lift, EHR Inventory) |

### What to Monitor

- `EHR messaging`
- `patient-chart messaging`
- `clinical trigger`
- `ICD-10 trigger`
- `CPT trigger`
- `NDC trigger`
- `ePrescribe placement`
- `POCMA`
- `point-of-care media`
- `workflow messaging`

### High-Signal Competitor Moves

- new EHR/ePrescribe partner
- POCMA certification
- patient chart messaging
- ICD/CPT/NDC trigger claims
- script-lift case study
- new clinical workflow surface
- integration into non-owned EHR networks

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent, Partnership / Integration Agent, Case Study / Proof Point Agent, Docs / Release Notes Agent

---

## 8. NEXT

**Journey / role:** Orchestration
**Doceree product essence:** AI omnichannel orchestration based on real-time clinical intent, with BYOP/open activation.

### Competitive Frame

This is a demand-side product. The competitive frame should include direct product competitors, adjacent platform competitors, data/identity competitors, activation competitors, and category-shaping entrants that could influence buyer perception or budget allocation.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| DeepIntent | [DeepIntent](https://deepintent.com/) | [Official](https://deepintent.com/)<br>[Monitor 1](https://deepintent.com/news)<br>[Monitor 2](https://deepintent.com/careers)<br>[Monitor 3](https://deepintent.com/solutions) | High / direct | 1 | Healthcare DSP | Cortex repositioning as orchestration parity with NEXT; Helix infrastructure; Place Exchange DOOH reach. | DeepIntent DSP, DeepIntent Cortex, DeepIntent Helix, MarketMatch Planner, Audience Marketplace |
| IQVIA | [IQVIA](https://www.iqvia.com/) | [Official](https://www.iqvia.com/)<br>[Monitor 1](https://www.iqvia.com/newsroom)<br>[Monitor 2](https://www.iqvia.com/solutions)<br>[Monitor 3](https://iqvia.wd1.myworkdayjobs.com/IQVIA/) | High / direct | 1 | Healthcare data, analytics, technology | Data-scale dominance; agentic-AI direction; Lasso-Doceree NEXT head-to-head. | NPA, NSP, MIDAS, OneKey, E360 RWD |
| IQVIA Digital | [IQVIA Digital](https://www.iqviadigital.com/) | [Official](https://www.iqviadigital.com/)<br>[Monitor 1](https://www.iqviadigital.com/solutions)<br>[Monitor 2](https://www.iqviadigital.com/resources)<br>[Monitor 3](https://www.iqviadigital.com/about-us/careers) | High / direct | 1 | Omnichannel healthcare marketing and analytics platform; legacy Lasso, now active as IQVIA Digital | Walled-garden alternative bundled with IQVIA data. | IQVIA Digital, legacy Lasso omnichannel healthcare marketing platform |
| OptimizeRx | [OptimizeRx](https://www.optimizerx.com/) | [Official](https://www.optimizerx.com/)<br>[Monitor 1](https://investors.optimizerx.com/news-releases)<br>[Monitor 2](https://www.optimizerx.com/blog)<br>[Monitor 3](https://www.optimizerx.com/careers) | Medium / adjacent | 1 | Point-of-care marketing; healthcare omnichannel | Direct head-to-head loss source on POC; DAAP can be misread as orchestration parity with NEXT; pharmacy-adjacent moves overlap with POD. | DAAP, Micro-Neighborhood Targeting, EHR/ePrescribe placements, Patient-chart messaging |
| PulsePoint | [PulsePoint](https://www.pulsepoint.com/) | [Official](https://www.pulsepoint.com/)<br>[Monitor 1](https://www.pulsepoint.com/resources/newsroom)<br>[Monitor 2](https://blog.pulsepoint.com/)<br>[Monitor 3](https://jobs.jobvite.com/pulsepoint/jobs) | Medium / adjacent | 1 | Healthcare programmatic; HCP measurement | Identity-layer competition via Medscape data; programmatic scale; HCP365 measurement. | PulsePoint platform, HCP365, Signal Platform, HCP Direct Match, HCP Explorer |
| Veradigm | [Veradigm](https://veradigm.com/) | [Official](https://veradigm.com/)<br>[Monitor 1](https://veradigm.com/about-veradigm/careers/join-our-team/)<br>[Monitor 2](https://veradigm.com/news/)<br>[Monitor 3](https://veradigm.com/solutions/) | Medium / adjacent | 1 | EHR ad media; healthcare data and provider-network tech | Strong incumbent on POC. | Veradigm Digital Health Media, Veradigm Network, Allscripts ambulatory EHRs |
| Komodo Health | [Komodo Health](https://www.komodohealth.com/) | [Official](https://www.komodohealth.com/)<br>[Monitor 1](https://www.komodohealth.com/solutions)<br>[Monitor 2](https://www.komodohealth.com/insights)<br>[Monitor 3](https://www.komodohealth.com/careers/life-at-komodo/) | Medium / adjacent | 2 | Healthcare data; Real-World Data | Marketplace data competitor; Marmot AI threatens NEXT positioning. | Healthcare Map, MapLab, MapLab Enterprise, MapView, MapExplorer |
| Relevate Health | [Relevate Health](https://www.relevatehealth.com/) | [Official](https://www.relevatehealth.com/)<br>[Monitor 1](https://www.relevatehealth.com/news)<br>[Monitor 2](https://www.relevatehealth.com/blogs/enhancing-hcp-customer-experience-within-the-ehr-workflow)<br>[Monitor 3](https://www.relevatehealth.com/careers) | Medium / adjacent | 2 | Pharma agency-tech hybrid | Direct POC competitor; agency-tech bundle attractive to brands looking for one vendor. | ELE Decision Engine, EHR-workflow-triggered messages, Level Ex pharma games |
| StackAdapt | [StackAdapt](https://www.stackadapt.com/) | [Official](https://www.stackadapt.com/)<br>[Monitor 1](https://www.stackadapt.com/our-solutions/npi-targeting-and-measurement)<br>[Monitor 2](https://www.stackadapt.com/resources)<br>[Monitor 3](https://www.stackadapt.com/careers) | Medium / adjacent | 2 | AI-powered programmatic | Self-serve programmatic alternative for pharma agencies. | StackAdapt platform, Healthcare suite (NPI Targeting, Script Lift, EHR Inventory) |
| Swoop | [Swoop](https://swoop.com/) | [Official](https://swoop.com/)<br>[Monitor 1](https://swoop.com/)<br>[Monitor 2](https://ats.rippling.com/swoopishiring/jobs) | Medium / adjacent | 2 | Predictive HCP / patient audience platform | Predictive audience competition. | Swoop omnichannel marketing platform, Swoop Piper |
| Trade Desk | [Trade Desk](https://www.thetradedesk.com/) | [Official](https://www.thetradedesk.com/)<br>[Monitor 1](https://www.thetradedesk.com/us/solutions)<br>[Monitor 2](https://www.thetradedesk.com/us/about-us/newsroom)<br>[Monitor 3](https://www.thetradedesk.com/us/careers) | Medium / adjacent | 2 | Independent omnichannel DSP; pharma marketplace | Direct Premium Programmatic competitor; also a BYOP integration partner. | TTD DSP, Sellers and Publishers 500+, OpenPath, HCP endemic pharma marketplace |
| CoverMyMeds | [CoverMyMeds](https://www.covermymeds.health/) | [Official](https://www.covermymeds.health/)<br>[Monitor 1](https://www.covermymeds.health/our-solutions)<br>[Monitor 2](https://www.covermymeds.health/about/newsroom)<br>[Monitor 3](https://talentcommunity.mckesson.com/flows/cmm) | Low / watchlist | 1 | Patient access; prior authorization; affordability | Workflow-incumbency; existing PA relationships difficult to displace. | PA platform, Benefits verification, Affordability and patient access products |
| Doximity | [Doximity](https://www.doximity.com/) | [Official](https://www.doximity.com/)<br>[Monitor 1](https://www.doximity.com/marketing-solutions)<br>[Monitor 2](https://press.doximity.com/)<br>[Monitor 3](https://www.doximity.com/careers) | Low / watchlist | 1 | HCP destination network; HCP advertising | HCP audience destination; DocsGPT competes with Site-specific LLM. | Doximity platform, DocsGPT, Doximity GPT for clinicians, Physician job marketplace, Telehealth |
| Medscape (WebMD Health) | [Medscape (WebMD Health)](https://www.medscapeglobal.com/) | [Official](https://www.medscapeglobal.com/)<br>[Monitor 1](https://www.medscape.com/)<br>[Monitor 2](https://www.webmd.com/mediakit)<br>[Monitor 3](https://jobs.jobvite.com/webmd/jobs) | Low / watchlist | 1 | HCP destination; CME; medical news | HCP destination; Authenticated NPI feeds PulsePoint. | Medscape platform, Medscape Extend, CME |
| OpenEvidence | [OpenEvidence](https://www.openevidence.com/) | [Official](https://www.openevidence.com/)<br>[Monitor 1](https://www.openevidence.com/) | Low / watchlist | 1 | Clinical AI for physicians | Diverts HCP attention from Doceree publisher network; absorbs AI-era query volume. | OpenEvidence platform, OpenEvidence DeepConsult |

### What to Monitor

- `omnichannel orchestration`
- `next best action`
- `dynamic audience`
- `clinical-intent orchestration`
- `BYOP`
- `real-time trigger`
- `personalization hub`
- `healthcare marketing OS`
- `AI media buying`
- `CRM integration`

### High-Signal Competitor Moves

- real-time omnichannel orchestration
- next-best-action product
- dynamic audiences
- AI media buying with clinical data
- open activation / BYOP claim
- CRM/DSP integration
- clinical-intent personalization

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent

---

## 9. Clinical Intent Signals

**Journey / role:** Orchestration / Measurement
**Doceree product essence:** Unified clinical, behavioral and engagement signal layer for per-NPI prescriber-readiness scoring.

### Competitive Frame

This is a demand-side product. The competitive frame should include direct product competitors, adjacent platform competitors, data/identity competitors, activation competitors, and category-shaping entrants that could influence buyer perception or budget allocation.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| IQVIA | [IQVIA](https://www.iqvia.com/) | [Official](https://www.iqvia.com/)<br>[Monitor 1](https://www.iqvia.com/newsroom)<br>[Monitor 2](https://www.iqvia.com/solutions)<br>[Monitor 3](https://iqvia.wd1.myworkdayjobs.com/IQVIA/) | High / direct | research | Direct data intelligence competitor | Life-sciences data, analytics, OneKey, RWD and AI products compete when buyers want intent/readiness scores. |  |
| Komodo Health | [Komodo Health](https://www.komodohealth.com/) | [Official](https://www.komodohealth.com/)<br>[Monitor 1](https://www.komodohealth.com/solutions)<br>[Monitor 2](https://www.komodohealth.com/insights)<br>[Monitor 3](https://www.komodohealth.com/careers/life-at-komodo/) | High / direct | research | Direct data intelligence competitor | Healthcare Map and patient journey intelligence can support clinical intent and predictive readiness. |  |
| DeepIntent | [DeepIntent](https://deepintent.com/) | [Official](https://deepintent.com/)<br>[Monitor 1](https://deepintent.com/news)<br>[Monitor 2](https://deepintent.com/careers)<br>[Monitor 3](https://deepintent.com/solutions) | Medium / adjacent | research | Activation + intent competitor | Cortex and health-intelligent media buying compete when intent is bundled with activation. |  |
| PulsePoint | [PulsePoint](https://www.pulsepoint.com/) | [Official](https://www.pulsepoint.com/)<br>[Monitor 1](https://www.pulsepoint.com/resources/newsroom)<br>[Monitor 2](https://blog.pulsepoint.com/)<br>[Monitor 3](https://jobs.jobvite.com/pulsepoint/jobs) | Medium / adjacent | research | Measurement + identity competitor | HCP365/HCP identity and measurement compete where NPI-level engagement measurement informs readiness. |  |
| Swoop | [Swoop](https://swoop.com/) | [Official](https://swoop.com/)<br>[Monitor 1](https://swoop.com/)<br>[Monitor 2](https://ats.rippling.com/swoopishiring/jobs) | Medium / adjacent | research | Predictive targeting competitor | Predictive audience and health data activation overlap when intent is translated into targeting. |  |
| Veeva Crossix | [Veeva Crossix](https://www.veeva.com/products/marketing-analytics/) | [Official](https://www.veeva.com/products/marketing-analytics/)<br>[Monitor 1](https://www.veeva.com/products/crossix-data-platform/)<br>[Monitor 2](https://veevacrossix.com/)<br>[Monitor 3](https://www.veeva.com/resources) | Medium / adjacent | research | Measurement-adjacent | Analytics and measurement layer adjacent to prescriber readiness and campaign impact. |  |

### What to Monitor

- `clinical intent`
- `prescriber readiness`
- `readiness score`
- `real-time signal`
- `EHR + behavioral + engagement`
- `predictive scoring`
- `HCP journey intelligence`
- `NPI-level signal`

### High-Signal Competitor Moves

- prescriber-readiness score
- real-time clinical intent signal
- multi-signal NPI score
- data marketplace for intent
- external signal syndication
- predictive clinical journey modeling

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent

---

## 10. co-pay.com

**Journey / role:** Access and Activation
**Doceree product essence:** Manufacturer-facing affordability, RTBC, ePA and AI enrollment inside the prescribing workflow.

### Competitive Frame

This is a demand-side product. The competitive frame should include direct product competitors, adjacent platform competitors, data/identity competitors, activation competitors, and category-shaping entrants that could influence buyer perception or budget allocation.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| ConnectiveRx | [ConnectiveRx](https://www.connectiverx.com/) | [Official](https://www.connectiverx.com/)<br>[Monitor 1](https://www.connectiverx.com/)<br>[Monitor 2](https://www.connectiverx.com/careers)<br>[Monitor 3](https://careers-connectiverx.icims.com/jobs/intro?mobile=true&needsRedirect=false) | High / direct | 1 | Patient affordability; co-pay coupons; hub services | Coupon-network incumbency. | Co-pay assistance, Coupon products, Clinically-integrated provider engagement network, Hub services |
| CoverMyMeds | [CoverMyMeds](https://www.covermymeds.health/) | [Official](https://www.covermymeds.health/)<br>[Monitor 1](https://www.covermymeds.health/our-solutions)<br>[Monitor 2](https://www.covermymeds.health/about/newsroom)<br>[Monitor 3](https://talentcommunity.mckesson.com/flows/cmm) | High / direct | 1 | Patient access; prior authorization; affordability | Workflow-incumbency; existing PA relationships difficult to displace. | PA platform, Benefits verification, Affordability and patient access products |
| IQVIA | [IQVIA](https://www.iqvia.com/) | [Official](https://www.iqvia.com/)<br>[Monitor 1](https://www.iqvia.com/newsroom)<br>[Monitor 2](https://www.iqvia.com/solutions)<br>[Monitor 3](https://iqvia.wd1.myworkdayjobs.com/IQVIA/) | Medium / adjacent | 1 | Healthcare data, analytics, technology | Data-scale dominance; agentic-AI direction; Lasso-Doceree NEXT head-to-head. | NPA, NSP, MIDAS, OneKey, E360 RWD |
| OptimizeRx | [OptimizeRx](https://www.optimizerx.com/) | [Official](https://www.optimizerx.com/)<br>[Monitor 1](https://investors.optimizerx.com/news-releases)<br>[Monitor 2](https://www.optimizerx.com/blog)<br>[Monitor 3](https://www.optimizerx.com/careers) | Medium / adjacent | 1 | Point-of-care marketing; healthcare omnichannel | Direct head-to-head loss source on POC; DAAP can be misread as orchestration parity with NEXT; pharmacy-adjacent moves overlap with POD. | DAAP, Micro-Neighborhood Targeting, EHR/ePrescribe placements, Patient-chart messaging |
| Veradigm | [Veradigm](https://veradigm.com/) | [Official](https://veradigm.com/)<br>[Monitor 1](https://veradigm.com/about-veradigm/careers/join-our-team/)<br>[Monitor 2](https://veradigm.com/news/)<br>[Monitor 3](https://veradigm.com/solutions/) | Medium / adjacent | 1 | EHR ad media; healthcare data and provider-network tech | Strong incumbent on POC. | Veradigm Digital Health Media, Veradigm Network, Allscripts ambulatory EHRs |
| GoodRx | [GoodRx](https://www.goodrx.com/) | [Official](https://www.goodrx.com/)<br>[Monitor 1](https://investors.goodrx.com/news-and-events/press-releases)<br>[Monitor 2](https://www.goodrx.com/about/careers) | Medium / adjacent | 2 | Consumer prescription savings | Brand-name consumer alternative. | GoodRx app and website, Coupons, Telehealth |
| Relevate Health | [Relevate Health](https://www.relevatehealth.com/) | [Official](https://www.relevatehealth.com/)<br>[Monitor 1](https://www.relevatehealth.com/news)<br>[Monitor 2](https://www.relevatehealth.com/blogs/enhancing-hcp-customer-experience-within-the-ehr-workflow)<br>[Monitor 3](https://www.relevatehealth.com/careers) | Medium / adjacent | 2 | Pharma agency-tech hybrid | Direct POC competitor; agency-tech bundle attractive to brands looking for one vendor. | ELE Decision Engine, EHR-workflow-triggered messages, Level Ex pharma games |
| DeepIntent | [DeepIntent](https://deepintent.com/) | [Official](https://deepintent.com/)<br>[Monitor 1](https://deepintent.com/news)<br>[Monitor 2](https://deepintent.com/careers)<br>[Monitor 3](https://deepintent.com/solutions) | Low / watchlist | 1 | Healthcare DSP | Cortex repositioning as orchestration parity with NEXT; Helix infrastructure; Place Exchange DOOH reach. | DeepIntent DSP, DeepIntent Cortex, DeepIntent Helix, MarketMatch Planner, Audience Marketplace |
| Komodo Health | [Komodo Health](https://www.komodohealth.com/) | [Official](https://www.komodohealth.com/)<br>[Monitor 1](https://www.komodohealth.com/solutions)<br>[Monitor 2](https://www.komodohealth.com/insights)<br>[Monitor 3](https://www.komodohealth.com/careers/life-at-komodo/) | Low / watchlist | 2 | Healthcare data; Real-World Data | Marketplace data competitor; Marmot AI threatens NEXT positioning. | Healthcare Map, MapLab, MapLab Enterprise, MapView, MapExplorer |
| RedSail Technologies | [RedSail Technologies](https://www.redsailtechnologies.com/) | [Official](https://www.redsailtechnologies.com/)<br>[Monitor 1](https://www.redsailtechnologies.com/press-releases)<br>[Monitor 2](https://www.pioneerrx.com/category/press-releases)<br>[Monitor 3](https://www.redsailtechnologies.com/careers) | Low / watchlist | 2 | Pharmacy software (PMS) | Vertical lock-in on independents; could expand to chains. | PioneerRx PMS, Axys LTC, QS/1, BestRx, PrimeCare |

### What to Monitor

- `co-pay`
- `copay`
- `RTBC`
- `electronic prior authorization`
- `ePA`
- `patient access`
- `affordability`
- `savings enrollment`
- `hub services`
- `benefit verification`
- `therapy start`

### High-Signal Competitor Moves

- ePA launch
- real-time benefit check expansion
- AI enrollment assistant
- manufacturer savings integration
- coverage/OOP workflow
- hub services automation
- EHR-native affordability tool

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent, Partnership / Integration Agent, Case Study / Proof Point Agent, Docs / Release Notes Agent

---

## 11. Point-of-Dispense

**Journey / role:** Adherence and Refills
**Doceree product essence:** Native PMS-triggered dispensing and refill/adherence messaging.

### Competitive Frame

This is a demand-side product. The competitive frame should include direct product competitors, adjacent platform competitors, data/identity competitors, activation competitors, and category-shaping entrants that could influence buyer perception or budget allocation.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| ConnectiveRx | [ConnectiveRx](https://www.connectiverx.com/) | [Official](https://www.connectiverx.com/)<br>[Monitor 1](https://www.connectiverx.com/)<br>[Monitor 2](https://www.connectiverx.com/careers)<br>[Monitor 3](https://careers-connectiverx.icims.com/jobs/intro?mobile=true&needsRedirect=false) | High / direct | 1 | Patient affordability; co-pay coupons; hub services | Coupon-network incumbency. | Co-pay assistance, Coupon products, Clinically-integrated provider engagement network, Hub services |
| RedSail Technologies | [RedSail Technologies](https://www.redsailtechnologies.com/) | [Official](https://www.redsailtechnologies.com/)<br>[Monitor 1](https://www.redsailtechnologies.com/press-releases)<br>[Monitor 2](https://www.pioneerrx.com/category/press-releases)<br>[Monitor 3](https://www.redsailtechnologies.com/careers) | High / direct | 2 | Pharmacy software (PMS) | Vertical lock-in on independents; could expand to chains. | PioneerRx PMS, Axys LTC, QS/1, BestRx, PrimeCare |
| CoverMyMeds | [CoverMyMeds](https://www.covermymeds.health/) | [Official](https://www.covermymeds.health/)<br>[Monitor 1](https://www.covermymeds.health/our-solutions)<br>[Monitor 2](https://www.covermymeds.health/about/newsroom)<br>[Monitor 3](https://talentcommunity.mckesson.com/flows/cmm) | Medium / adjacent | 1 | Patient access; prior authorization; affordability | Workflow-incumbency; existing PA relationships difficult to displace. | PA platform, Benefits verification, Affordability and patient access products |
| OptimizeRx | [OptimizeRx](https://www.optimizerx.com/) | [Official](https://www.optimizerx.com/)<br>[Monitor 1](https://investors.optimizerx.com/news-releases)<br>[Monitor 2](https://www.optimizerx.com/blog)<br>[Monitor 3](https://www.optimizerx.com/careers) | Medium / adjacent | 1 | Point-of-care marketing; healthcare omnichannel | Direct head-to-head loss source on POC; DAAP can be misread as orchestration parity with NEXT; pharmacy-adjacent moves overlap with POD. | DAAP, Micro-Neighborhood Targeting, EHR/ePrescribe placements, Patient-chart messaging |
| IQVIA | [IQVIA](https://www.iqvia.com/) | [Official](https://www.iqvia.com/)<br>[Monitor 1](https://www.iqvia.com/newsroom)<br>[Monitor 2](https://www.iqvia.com/solutions)<br>[Monitor 3](https://iqvia.wd1.myworkdayjobs.com/IQVIA/) | Low / watchlist | 1 | Healthcare data, analytics, technology | Data-scale dominance; agentic-AI direction; Lasso-Doceree NEXT head-to-head. | NPA, NSP, MIDAS, OneKey, E360 RWD |
| GoodRx | [GoodRx](https://www.goodrx.com/) | [Official](https://www.goodrx.com/)<br>[Monitor 1](https://investors.goodrx.com/news-and-events/press-releases)<br>[Monitor 2](https://www.goodrx.com/about/careers) | Low / watchlist | 2 | Consumer prescription savings | Brand-name consumer alternative. | GoodRx app and website, Coupons, Telehealth |

### What to Monitor

- `PMS`
- `pharmacy management system`
- `NDC trigger`
- `dispense`
- `switch block`
- `refill adherence`
- `pharmacist messaging`
- `coupon printer`
- `first fill`
- `abandonment`

### High-Signal Competitor Moves

- PMS integration
- pharmacy workflow message
- NDC-triggered offer
- adherence SMS/refill loop
- new pharmacy network partnership
- coupon printer replacement
- pharmacist engagement product

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent, Partnership / Integration Agent, Case Study / Proof Point Agent, Docs / Release Notes Agent

---

## 12. Admanager

**Journey / role:** Supply: publisher monetization
**Doceree product essence:** Healthcare-exclusive ad server and monetization platform for medical publishers.

### Competitive Frame

This is a supply-side product. The competitive frame is not only other pharma-marketing platforms; it includes the platform owners, infrastructure providers, ad servers, clinical workflow companies, screen networks, pharmacy software vendors, and AI/content monetization systems that could capture the same supply-side economics.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| Google Ad Manager | [Google Ad Manager](https://admanager.google.com/home/) | [Official](https://admanager.google.com/home/)<br>[Monitor 1](https://admanager.google.com/home/)<br>[Monitor 2](https://support.google.com/admanager/)<br>[Monitor 3](https://publishersonair.withgoogle.com/ad-manager-getting-started) | High / direct | research | Direct ad-server benchmark | Default generic ad server benchmark for publishers; competes on workflow, trafficking, yield, and ad ops. |  |
| AdButler | [AdButler](https://www.adbutler.com/) | [Official](https://www.adbutler.com/)<br>[Monitor 1](https://www.adbutler.com/display-ad-server/)<br>[Monitor 2](https://help.adbutler.com/) | Medium / adjacent | research | Generic ad-server benchmark | Generic ad-server alternative for publishers; lacks healthcare-specific identity and demand. |  |
| Kevel | [Kevel](https://www.kevel.com/) | [Official](https://www.kevel.com/)<br>[Monitor 1](https://www.kevel.com/ad-server)<br>[Monitor 2](https://dev.kevel.com/reference/getting-started-with-kevel) | Medium / adjacent | research | Ad infrastructure benchmark | Ad-serving infrastructure benchmark for custom ad products. |  |
| PubMatic | [PubMatic](https://pubmatic.com/) | [Official](https://pubmatic.com/)<br>[Monitor 1](https://pubmatic.com/about-us/)<br>[Monitor 2](https://pubmatic.com/news/)<br>[Monitor 3](https://pubmatic.com/solutions/mobile/) | Medium / adjacent | research | Generic SSP benchmark | Programmatic monetization/SSP benchmark for publishers. |  |
| Smaato | [Smaato](https://www.smaato.com/) | [Official](https://www.smaato.com/)<br>[Monitor 1](https://www.smaato.com/company/)<br>[Monitor 2](https://www.smaato.com/publishers/)<br>[Monitor 3](https://verve.com/brand-marketplace-for-publishers/) | Medium / adjacent | research | Generic SSP benchmark | Programmatic ad-tech/SSP benchmark for mobile/in-app supply. |  |
| Magnite | [Magnite](https://www.magnite.com/) | [Official](https://www.magnite.com/)<br>[Monitor 1](https://www.magnite.com/press/)<br>[Monitor 2](https://www.magnite.com/about-us/) | Low / watchlist | research | Programmatic supply benchmark | Large SSP benchmark; less healthcare-specific. |  |

### What to Monitor

- `healthcare ad server`
- `publisher monetization`
- `HCP identity`
- `ad ops`
- `SSP`
- `publisher yield`
- `healthcare demand`
- `direct-sold campaigns`
- `one-script integration`

### High-Signal Competitor Moves

- healthcare ad server
- HCP identity for publishers
- new publisher monetization platform
- SSP integration for medical publishers
- one-script healthcare monetization
- direct-sold HCP analytics

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent, Partnership / Integration Agent, Case Study / Proof Point Agent, SEO / Category Narrative Agent (approved source pages only)

---

## 13. Publisher AI Suite

**Journey / role:** Supply: AI-era publisher engagement/protection
**Doceree product essence:** Site-specific LLM, AI ads and licensed content marketplace for medical publishers.

### Competitive Frame

This is a supply-side product. The competitive frame is not only other pharma-marketing platforms; it includes the platform owners, infrastructure providers, ad servers, clinical workflow companies, screen networks, pharmacy software vendors, and AI/content monetization systems that could capture the same supply-side economics.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| Doximity | [Doximity](https://www.doximity.com/) | [Official](https://www.doximity.com/)<br>[Monitor 1](https://www.doximity.com/marketing-solutions)<br>[Monitor 2](https://press.doximity.com/)<br>[Monitor 3](https://www.doximity.com/careers) | High / direct | research | Direct HCP network competitor | Physician network and AI/content engagement destination; competes for verified HCP attention. |  |
| Medscape / WebMD Health | [Medscape / WebMD Health](https://www.medscapeglobal.com/) | [Official](https://www.medscapeglobal.com/)<br>[Monitor 1](https://www.medscape.com/)<br>[Monitor 2](https://www.webmd.com/mediakit)<br>[Monitor 3](https://jobs.jobvite.com/webmd/jobs) | High / direct | research | Direct HCP content destination | Established HCP content destination; competes as a medical content and HCP engagement platform. |  |
| OpenEvidence | [OpenEvidence](https://www.openevidence.com/) | [Official](https://www.openevidence.com/)<br>[Monitor 1](https://www.openevidence.com/) | High / direct | research | Direct attention/category competitor | Medical AI answer engine and HCP destination; competes for HCP attention and publisher traffic behavior. |  |
| CCC | [CCC](https://www.copyright.com/) | [Official](https://www.copyright.com/)<br>[Monitor 1](https://www.copyright.com/solutions/)<br>[Monitor 2](https://www.copyright.com/news/) | Medium / adjacent | research | Rights/licensing infrastructure | Rights, licensing and content-usage infrastructure; relevant to licensed content marketplace. |  |
| Dappier | [Dappier](https://dappier.com/) | [Official](https://dappier.com/)<br>[Monitor 1](https://dappier.com/)<br>[Monitor 2](https://docs.dappier.com/publish-and-monetize) | Medium / adjacent | research | AI content monetization competitor | AI content monetization / marketplace tooling for publishers. |  |
| TollBit | [TollBit](https://tollbit.com/) | [Official](https://tollbit.com/)<br>[Monitor 1](https://tollbit.com/licensing-platform/)<br>[Monitor 2](https://docs.tollbit.com/docs/monetization) | Medium / adjacent | research | AI content licensing competitor | AI-era publisher content licensing / bot monetization infrastructure. |  |
| UpToDate / Wolters Kluwer | [UpToDate / Wolters Kluwer](https://www.wolterskluwer.com/en/solutions/uptodate) | [Official](https://www.wolterskluwer.com/en/solutions/uptodate)<br>[Monitor 1](https://www.wolterskluwer.com/en/solutions/uptodate/about)<br>[Monitor 2](https://www.uptodate.com/login) | Medium / adjacent | research | Clinical reference competitor | Clinical decision content destination; competes for professional medical information time. |  |

### What to Monitor

- `site-specific LLM`
- `AI ads`
- `content licensing`
- `licensed content marketplace`
- `AI search traffic loss`
- `bot monetization`
- `publisher AI assistant`
- `HCP chatbot`
- `medical AI answer engine`

### High-Signal Competitor Moves

- medical publisher AI assistant
- AI ad inventory
- licensed content marketplace
- bot/content scraping monetization
- publisher content licensing partnership
- HCP AI answer engine

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent, Approved Social Intelligence Agent (approved sources only), Analyst / Market Report Agent (manual uploads only), Category Narrative Classifier, Partnership / Integration Agent, Case Study / Proof Point Agent, SEO / Category Narrative Agent (approved source pages only)

---

## 14. Spark for EHRs

**Journey / role:** Supply: EHR clinical messaging infrastructure
**Doceree product essence:** EHR-vendor monetization modules for co-pay assistance, drug education, clinical trial recruitment and workflow messaging.

### Competitive Frame

This is a supply-side product. The competitive frame is not only other pharma-marketing platforms; it includes the platform owners, infrastructure providers, ad servers, clinical workflow companies, screen networks, pharmacy software vendors, and AI/content monetization systems that could capture the same supply-side economics.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| OptimizeRx | [OptimizeRx](https://www.optimizerx.com/) | [Official](https://www.optimizerx.com/)<br>[Monitor 1](https://investors.optimizerx.com/news-releases)<br>[Monitor 2](https://www.optimizerx.com/blog)<br>[Monitor 3](https://www.optimizerx.com/careers) | High / direct | research | Direct EHR monetization competitor | Large EHR/ePrescribe partner network and patient-chart messaging; direct EHR workflow monetization competitor. |  |
| Veradigm | [Veradigm](https://veradigm.com/) | [Official](https://veradigm.com/)<br>[Monitor 1](https://veradigm.com/about-veradigm/careers/join-our-team/)<br>[Monitor 2](https://veradigm.com/news/)<br>[Monitor 3](https://veradigm.com/solutions/) | High / direct | research | Direct EHR network competitor | Owns EHR ecosystem and digital health media placements; direct clinical workflow media competitor. |  |
| PrescriberPoint | [PrescriberPoint](https://prescriberpoint.com/) | [Official](https://prescriberpoint.com/)<br>[Monitor 1](https://prescriberpoint.com/prescriber-ai)<br>[Monitor 2](https://prescriberpoint.com/insights/introducing-prescriberai)<br>[Monitor 3](https://prescriberpointwebapps.com/signup) | Medium / adjacent | research | POC workflow-adjacent | AI-powered point-of-care platform supporting clinical info, coverage, PA and savings workflows. |  |
| Relevate Health | [Relevate Health](https://www.relevatehealth.com/) | [Official](https://www.relevatehealth.com/)<br>[Monitor 1](https://www.relevatehealth.com/news)<br>[Monitor 2](https://www.relevatehealth.com/blogs/enhancing-hcp-customer-experience-within-the-ehr-workflow)<br>[Monitor 3](https://www.relevatehealth.com/careers) | Medium / adjacent | research | POC/EHR-adjacent | Point-of-care / provider engagement competitor with EHR-adjacent capabilities. |  |
| DeepIntent | [DeepIntent](https://deepintent.com/) | [Official](https://deepintent.com/)<br>[Monitor 1](https://deepintent.com/news)<br>[Monitor 2](https://deepintent.com/careers)<br>[Monitor 3](https://deepintent.com/solutions) | Low / watchlist | research | DSP adjacent | Healthcare DSP can compete when EHR/workflow or POC inventory partnerships appear. |  |

### What to Monitor

- `SMART on FHIR`
- `EHR vendor monetization`
- `clinical messaging module`
- `in-workflow pharma demand`
- `trial recruitment EHR`
- `drug education EHR`
- `co-pay EHR module`

### High-Signal Competitor Moves

- EHR vendor monetization product
- SMART on FHIR clinical messaging
- drug education module in EHR
- clinical trial recruitment module
- affordability module inside EHR
- exclusive EHR ad network

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent, Partnership / Integration Agent, Case Study / Proof Point Agent, Docs / Release Notes Agent

---

## 15. Spark for DOOH

**Journey / role:** Supply: clinical-screen DOOH
**Doceree product essence:** Software layer for patient-level clinical screen targeting using EHR check-in data.

### Competitive Frame

This is a supply-side product. The competitive frame is not only other pharma-marketing platforms; it includes the platform owners, infrastructure providers, ad servers, clinical workflow companies, screen networks, pharmacy software vendors, and AI/content monetization systems that could capture the same supply-side economics.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| CheckedUp | [CheckedUp](https://www.checkedup.com/) | [Official](https://www.checkedup.com/)<br>[Monitor 1](https://www.checkedup.com/solutions/)<br>[Monitor 2](https://www.checkedup.com/about-us/) | High / direct | research | Direct owned network | Point-of-care screen network; direct clinical waiting-room/screen inventory competitor. |  |
| PatientPoint | [PatientPoint](https://patientpoint.com/) | [Official](https://patientpoint.com/)<br>[Monitor 1](https://careers.patientpoint.com/)<br>[Monitor 2](https://careers.patientpoint.com/search/searchjobs)<br>[Monitor 3](https://patientpoint.com/) | High / direct | research | Direct owned network | Owned point-of-care screen/office network; major direct DOOH/POC screen competitor. |  |
| DeepIntent via Place Exchange | [DeepIntent via Place Exchange](https://deepintent.com/) | [Official](https://deepintent.com/)<br>[Monitor 1](https://www.placeexchange.com/)<br>[Monitor 2](https://deepintent.com/news) | Medium / adjacent | research | Healthcare DSP + DOOH | Healthcare DSP + DOOH partnership signal; monitor for clinical-screen or patient targeting depth. |  |
| Place Exchange | [Place Exchange](https://www.placeexchange.com/) | [Official](https://www.placeexchange.com/)<br>[Monitor 1](https://www.placeexchange.com/news)<br>[Monitor 2](https://www.placeexchange.com/about) | Medium / adjacent | research | Programmatic DOOH exchange | Programmatic DOOH exchange; relevant where healthcare inventory is activated through DOOH pipes. |  |
| Screenverse | [Screenverse](https://www.screenversemedia.com/) | [Official](https://www.screenversemedia.com/)<br>[Monitor 1](https://www.screenversemedia.com/services/digital-billboards)<br>[Monitor 2](https://www.screenversemedia.com/blog) | Medium / adjacent | research | DOOH monetization benchmark | DOOH network monetization / programmatic sales benchmark. |  |
| Vistar Media | [Vistar Media](https://www.vistarmedia.com/) | [Official](https://www.vistarmedia.com/)<br>[Monitor 1](https://www.vistarmedia.com/news)<br>[Monitor 2](https://www.vistarmedia.com/blog)<br>[Monitor 3](https://www.vistarmedia.com/careers) | Medium / adjacent | research | Programmatic DOOH benchmark | Programmatic DOOH platform; benchmark for DOOH activation and buyer workflows. |  |

### What to Monitor

- `DOOH`
- `clinical screens`
- `waiting room screens`
- `EHR check-in`
- `patient screen targeting`
- `programmatic DOOH`
- `Place Exchange`
- `screen network`
- `POC screens`

### High-Signal Competitor Moves

- clinical-screen network expansion
- programmatic DOOH healthcare activation
- EHR check-in data targeting
- waiting-room screen partner
- patient-level DOOH measurement
- screen network pharma demand

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent, Partnership / Integration Agent, Case Study / Proof Point Agent, SEO / Category Narrative Agent (approved source pages only)

---

## 16. Spark for Pharmacy

**Journey / role:** Supply: pharmacy software monetization
**Doceree product essence:** Embedded POD modules for PMS vendors with built-in pharma demand.

### Competitive Frame

This is a supply-side product. The competitive frame is not only other pharma-marketing platforms; it includes the platform owners, infrastructure providers, ad servers, clinical workflow companies, screen networks, pharmacy software vendors, and AI/content monetization systems that could capture the same supply-side economics.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| ConnectiveRx | [ConnectiveRx](https://www.connectiverx.com/) | [Official](https://www.connectiverx.com/)<br>[Monitor 1](https://www.connectiverx.com/)<br>[Monitor 2](https://www.connectiverx.com/careers)<br>[Monitor 3](https://careers-connectiverx.icims.com/jobs/intro?mobile=true&needsRedirect=false) | High / direct | research | Direct patient access + pharmacy workflow | Patient affordability and pharmacy workflow solutions with overlap in dispense/adherence. |  |
| RedSail Technologies / PioneerRx | [RedSail Technologies / PioneerRx](https://www.redsailtechnologies.com/) | [Official](https://www.redsailtechnologies.com/)<br>[Monitor 1](https://www.pioneerrx.com/)<br>[Monitor 2](https://www.pioneerrx.com/category/press-releases)<br>[Monitor 3](https://www.redsailtechnologies.com/press-releases) | High / direct | research | Direct PMS competitor | Vertical PMS owner with pharmacy software footprint; direct lock-in risk for PMS monetization. |  |
| RelayHealth / Change Healthcare / Optum Insight | [RelayHealth / Change Healthcare / Optum Insight](https://business.optum.com/en/optum-insight.html) | [Official](https://business.optum.com/en/optum-insight.html)<br>[Monitor 1](https://www.changehealthcare.com/)<br>[Monitor 2](https://business.optum.com/en/optum-insight.html)<br>[Monitor 3](https://www.optum.com/en/about-us/careers.html) | High / direct | research | Pharmacy network infrastructure | Pharmacy connectivity and claims infrastructure; relevant to PMS/dispense workflow access. |  |
| CoverMyMeds | [CoverMyMeds](https://www.covermymeds.health/) | [Official](https://www.covermymeds.health/)<br>[Monitor 1](https://www.covermymeds.health/our-solutions)<br>[Monitor 2](https://www.covermymeds.health/about/newsroom)<br>[Monitor 3](https://talentcommunity.mckesson.com/flows/cmm) | Medium / adjacent | research | Access network adjacent | ePA/access network; relevant where pharmacy/PBM/prescribing workflow intersects. |  |
| DrFirst | [DrFirst](https://drfirst.com/) | [Official](https://drfirst.com/)<br>[Monitor 1](https://drfirst.com/solutions/)<br>[Monitor 2](https://drfirst.com/news/)<br>[Monitor 3](https://drfirst.com/careers/) | Medium / adjacent | research | Medication workflow adjacent | e-prescribing and medication management workflow; monitor for affordability/pharmacy activation. |  |
| MedAdvisor | [MedAdvisor](https://www.medadvisor.com/) | [Official](https://www.medadvisor.com/)<br>[Monitor 1](https://www.medadvisor.com/)<br>[Monitor 2](https://www.medadvisor.com/news/) | Medium / adjacent | research | Pharmacy engagement competitor | Pharmacy adherence and patient engagement competitor; post-MVP source discovery. |  |
| OptimizeRx | [OptimizeRx](https://www.optimizerx.com/) | [Official](https://www.optimizerx.com/)<br>[Monitor 1](https://investors.optimizerx.com/news-releases)<br>[Monitor 2](https://www.optimizerx.com/blog)<br>[Monitor 3](https://www.optimizerx.com/careers) | Medium / adjacent | research | POC/pharmacy adjacent | Retail/pharmacy-adjacent expansion signals overlap with Spark for Pharmacy. |  |

### What to Monitor

- `PMS vendor`
- `pharmacy software`
- `PioneerRx`
- `NDC trigger`
- `pharmacy workflow monetization`
- `pharmacist message`
- `PMS integration`
- `independent pharmacies`

### High-Signal Competitor Moves

- PMS vendor monetization
- pharmacy software ads
- PioneerRx / RedSail product expansion
- NDC-triggered workflow
- adherence/refill messaging
- pharmacy network exclusivity

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent, Partnership / Integration Agent, Case Study / Proof Point Agent, Docs / Release Notes Agent

---

## 17. co-pay.com for Health Systems

**Journey / role:** Supply: health-system access
**Doceree product essence:** Health-system-side affordability and access workflow funded by manufacturers.

### Competitive Frame

This is a supply-side product. The competitive frame is not only other pharma-marketing platforms; it includes the platform owners, infrastructure providers, ad servers, clinical workflow companies, screen networks, pharmacy software vendors, and AI/content monetization systems that could capture the same supply-side economics.

### Competitor Split

| Competitor | Primary URL | Key URLs to Monitor | Threat Level | Tier / Status | Category | Why It Matters | Known Products / Source Notes |
|---|---|---|---|---|---|---|---|
| ConnectiveRx | [ConnectiveRx](https://www.connectiverx.com/) | [Official](https://www.connectiverx.com/)<br>[Monitor 1](https://www.connectiverx.com/)<br>[Monitor 2](https://www.connectiverx.com/careers)<br>[Monitor 3](https://careers-connectiverx.icims.com/jobs/intro?mobile=true&needsRedirect=false) | High / direct | research | Direct access competitor | Patient support, affordability, enrollment and access competitor. |  |
| CoverMyMeds | [CoverMyMeds](https://www.covermymeds.health/) | [Official](https://www.covermymeds.health/)<br>[Monitor 1](https://www.covermymeds.health/our-solutions)<br>[Monitor 2](https://www.covermymeds.health/about/newsroom)<br>[Monitor 3](https://talentcommunity.mckesson.com/flows/cmm) | High / direct | research | Direct access competitor | ePA and access platform; strong access workflow competitor. |  |
| OptimizeRx | [OptimizeRx](https://www.optimizerx.com/) | [Official](https://www.optimizerx.com/)<br>[Monitor 1](https://investors.optimizerx.com/news-releases)<br>[Monitor 2](https://www.optimizerx.com/blog)<br>[Monitor 3](https://www.optimizerx.com/careers) | High / direct | research | Direct workflow competitor | EHR/ePrescribe partner network and affordability/clinical messaging overlap. |  |
| Veradigm | [Veradigm](https://veradigm.com/) | [Official](https://veradigm.com/)<br>[Monitor 1](https://veradigm.com/about-veradigm/careers/join-our-team/)<br>[Monitor 2](https://veradigm.com/news/)<br>[Monitor 3](https://veradigm.com/solutions/) | High / direct | research | Direct EHR workflow competitor | EHR network and digital health media; can deliver access/support messages in workflow. |  |
| AssistRx | [AssistRx](https://www.assistrx.com/) | [Official](https://www.assistrx.com/)<br>[Monitor 1](https://www.assistrx.com/specialty-pharmaceutical-solutions/)<br>[Monitor 2](https://www.assistrx.com/specialty-pharmaceutical-solutions/assistrx-patient-solutions/)<br>[Monitor 3](https://www.assistrx.com/careers) | Medium / adjacent | research | Patient access competitor | Patient support and access hub competitor. |  |
| PrescriberPoint | [PrescriberPoint](https://prescriberpoint.com/) | [Official](https://prescriberpoint.com/)<br>[Monitor 1](https://prescriberpoint.com/prescriber-ai)<br>[Monitor 2](https://prescriberpoint.com/insights/introducing-prescriberai)<br>[Monitor 3](https://prescriberpointwebapps.com/signup) | Medium / adjacent | research | POC access competitor | Point-of-care prescribing support, PA, out-of-pocket and savings workflow. |  |
| Relevate Health | [Relevate Health](https://www.relevatehealth.com/) | [Official](https://www.relevatehealth.com/)<br>[Monitor 1](https://www.relevatehealth.com/news)<br>[Monitor 2](https://www.relevatehealth.com/blogs/enhancing-hcp-customer-experience-within-the-ehr-workflow)<br>[Monitor 3](https://www.relevatehealth.com/careers) | Medium / adjacent | research | POC access-adjacent | POC provider engagement and clinical decision support adjacency. |  |
| Surescripts | [Surescripts](https://surescripts.com/) | [Official](https://surescripts.com/)<br>[Monitor 1](https://surescripts.com/solutions)<br>[Monitor 2](https://surescripts.com/news-center)<br>[Monitor 3](https://surescripts.com/careers) | Medium / adjacent | research | Infrastructure competitor | e-prescribing and prior authorization network; infrastructure competitor. |  |

### What to Monitor

- `health system affordability`
- `EHR-native co-pay`
- `prior authorization workflow`
- `IDN access`
- `manufacturer-funded support`
- `care-team burden`
- `savings programs inside EHR`

### High-Signal Competitor Moves

- health-system affordability workflow
- EHR-native savings programs
- care-team burden reduction
- manufacturer-funded health-system workflow
- AI enrollment inside EHR
- IDN access solution

### Battlecard Questions

- What exact competitor claim is being made, and on which source?
- Does this competitor claim overlap with the same buyer, same workflow, or same budget as this Doceree product?
- Is the competitor claiming a shipped capability, a roadmap, a partnership, a case study, or thought leadership?
- What Doceree proof point is needed to respond safely?
- Is this a sales objection, an executive concern, a PMM action item, or just a monitoring signal?
- What caveat must be preserved based on the source type?

### Suggested Monitoring Agents

Website Change Hunter, News / PR Agent, Jobs Signal Agent, Product Mapper, Severity Scorer, Confidence Scorer, Overclaiming Guardrail, Duplicate Detector, Daily Brief Agent, Partnership / Integration Agent, Case Study / Proof Point Agent, Docs / Release Notes Agent

---

# Competitor Profile Appendix

This appendix normalizes competitors into CI Command Center fields. For active MVP competitors, source rows should be loaded from the registry. For post-MVP and research-discovered competitors, create source-discovery backlog items until Sherry validates URLs and priority.

## 6sense

- **Tier:** 2
- **Website:** https://6sense.com/
- **Category:** Generic B2B ABM with AI
- **Short description:** 6sense Revenue AI — predictive scoring, intent across 40+ languages, AI agents for GTM tasks.
- **Reason for monitoring:** Generic ABM benchmark; AI/agent expansion notable.
- **Known products:** 6sense Revenue AI, AI agents for GTM tasks
- **Positioning summary:** The ABM Platform Powered by Revenue Intelligence.
- **Potential threat:** AI agent direction overlaps RepTwin if extended to healthcare.
- **Information gaps:** Healthcare module roadmap

| Product | Overlap |
|---|---:|
| Marketplace | N |
| ABM | M |
| Premium Programmatic | N |
| RepTwin | N |
| Point-of-Care | N |
| NEXT | N |
| co-pay.com | N |
| Point-of-Dispense | N |

**Registry sources to monitor:**
- Newsroom — https://6sense.com/news/ (Newsroom; priority 2; Weekly; Sitemap monitor; confidence High)
- Blog — https://6sense.com/blog/ (Blog; priority 2; Weekly; RSS feed; confidence High)

## ConnectiveRx

- **Tier:** 1
- **Website:** https://www.connectiverx.com/
- **Category:** Patient affordability; co-pay coupons; hub services
- **Short description:** Co-pay assistance, hub services, branded co-pay coupons via PoC, e-prescribing, pharmacy. Activated 1.2M providers via clinically-embedded PoC network.
- **Reason for monitoring:** Most-named POD/co-pay competitor.
- **Known products:** Co-pay assistance, Coupon products, Clinically-integrated provider engagement network, Hub services
- **Positioning summary:** Patient access and affordability; clinically-embedded reach.
- **Potential threat:** Coupon-network incumbency.
- **Information gaps:** Real-time vs aggregated workflow activation

| Product | Overlap |
|---|---:|
| Marketplace | N |
| ABM | N |
| Premium Programmatic | N |
| RepTwin | N |
| Point-of-Care | M |
| NEXT | N |
| co-pay.com | H |
| Point-of-Dispense | H |

**Registry sources to monitor:**
- Homepage — https://www.connectiverx.com/ (Homepage; priority 1; Daily; Website crawler; confidence High)
- Thought leadership / press — https://www.connectiverx.com/thought-leadership (Press / blog; priority 1; Daily; Website crawler; confidence High)
- Talent ATS — https://talent.connectiverx.com/jobs (Careers; priority 2; Weekly; Website crawler; confidence High)

## CoverMyMeds

- **Tier:** 1
- **Website:** https://www.covermymeds.com/
- **Category:** Patient access; prior authorization; affordability
- **Short description:** McKesson subsidiary; largest US PA platform; integrates with EHRs and pharmacies.
- **Reason for monitoring:** Most-named co-pay.com competitor.
- **Known products:** PA platform, Benefits verification, Affordability and patient access products
- **Positioning summary:** Help People Get the Medicine They Need.
- **Potential threat:** Workflow-incumbency; existing PA relationships difficult to displace.
- **Information gaps:** AI / ePA roadmap, Workflow comparison vs co-pay.com integrated bundle

| Product | Overlap |
|---|---:|
| Marketplace | L |
| ABM | N |
| Premium Programmatic | N |
| RepTwin | N |
| Point-of-Care | M |
| NEXT | L |
| co-pay.com | H |
| Point-of-Dispense | M |

**Registry sources to monitor:**
- Homepage — https://www.covermymeds.com/ (Homepage; priority 1; Daily; Website crawler; confidence High)
- Press — https://insights.covermymeds.com/press (Newsroom; priority 1; Daily; Website crawler; confidence High)
- Open positions — https://experience.covermymeds.com/open-positions (Careers; priority 2; Weekly; Website crawler; confidence High)

## DeepIntent

- **Tier:** 1
- **Website:** https://deepintent.com/
- **Category:** Healthcare DSP
- **Short description:** Healthcare-specific DSP. DeepIntent Cortex (AI media buying); DeepIntent Helix (HIPAA-ready cloud). $637M Vitruvian investment Sep 2025.
- **Reason for monitoring:** Most-named Premium Programmatic / NEXT competitor.
- **Known products:** DeepIntent DSP, DeepIntent Cortex, DeepIntent Helix, MarketMatch Planner, Audience Marketplace, Data HealthChecks
- **Positioning summary:** Healthcare Marketing Demand Side Platform / Health Intelligent media buying.
- **Potential threat:** Cortex repositioning as orchestration parity with NEXT; Helix infrastructure; Place Exchange DOOH reach.
- **Information gaps:** Cortex vs NEXT feature parity, Helix scope vs Doceree compliance posture, Place Exchange clinical-screen depth

| Product | Overlap |
|---|---:|
| Marketplace | M |
| ABM | N |
| Premium Programmatic | H |
| RepTwin | L |
| Point-of-Care | M |
| NEXT | H |
| co-pay.com | L |
| Point-of-Dispense | N |

**Registry sources to monitor:**
- Homepage — https://deepintent.com/ (Homepage; priority 1; Daily; Website crawler; confidence High)
- News — https://deepintent.com/news (Newsroom; priority 1; Daily; Sitemap monitor; confidence High)
- About / News archive — https://www.deepintent.com/about/news/ (Newsroom; priority 1; Daily; Website crawler; confidence High)
- Start.deepintent news — https://start.deepintent.com/news/ (Newsroom; priority 2; Weekly; Website crawler; confidence High)

## Definitive Healthcare

- **Tier:** 2
- **Website:** https://www.definitivehc.com/
- **Category:** Healthcare commercial intelligence
- **Short description:** Public company. View Suite, Monocl, Carevoyance, Populi. Founded 2011.
- **Reason for monitoring:** Marketplace competitor; also a Doceree ABM partner — dual relationship.
- **Known products:** View Suite, Monocl Expert, Carevoyance, Populi, APIs
- **Positioning summary:** Healthcare Commercial Intelligence.
- **Potential threat:** Marketplace data competitor.
- **Information gaps:** Activation roadmap, AI roadmap

| Product | Overlap |
|---|---:|
| Marketplace | H |
| ABM | M |
| Premium Programmatic | N |
| RepTwin | N |
| Point-of-Care | N |
| NEXT | N |
| co-pay.com | N |
| Point-of-Dispense | N |

**Registry sources to monitor:**
- Homepage — https://www.definitivehc.com/ (Homepage; priority 1; Daily; Website crawler; confidence High)
- Press — https://www.definitivehc.com/about/press (Newsroom; priority 1; Daily; Sitemap monitor; confidence High)
- Blog — https://www.definitivehc.com/blog (Blog; priority 2; Weekly; RSS feed; confidence High)

## Demandbase

- **Tier:** 2
- **Website:** https://www.demandbase.com/
- **Category:** Generic B2B ABM
- **Short description:** Demandbase One ABX platform — account intelligence, intent, programmatic, sales orchestration.
- **Reason for monitoring:** Generic ABM benchmark; entry into healthcare would escalate priority.
- **Known products:** Demandbase One
- **Positioning summary:** ABM Platform for B2B Sales & Marketing Success.
- **Potential threat:** If launches a healthcare module, threat escalates.
- **Information gaps:** Healthcare-specific roadmap

| Product | Overlap |
|---|---:|
| Marketplace | N |
| ABM | M |
| Premium Programmatic | N |
| RepTwin | N |
| Point-of-Care | N |
| NEXT | N |
| co-pay.com | N |
| Point-of-Dispense | N |

**Registry sources to monitor:**
- Newsroom — https://www.demandbase.com/about-us/news/ (Newsroom; priority 2; Weekly; Sitemap monitor; confidence High)
- Blog — https://www.demandbase.com/blog/ (Blog; priority 2; Weekly; RSS feed; confidence High)

## Doximity

- **Tier:** 1
- **Website:** https://www.doximity.com/
- **Category:** HCP destination network; HCP advertising
- **Short description:** Largest US digital network of medical professionals (~80% of US physicians). DocsGPT AI features; pharma marketing solutions.
- **Reason for monitoring:** Anchor competitor for Publisher AI Suite.
- **Known products:** Doximity platform, DocsGPT, Doximity GPT for clinicians, Physician job marketplace, Telehealth, Pharma marketing solutions
- **Positioning summary:** Largest US digital network of medical professionals.
- **Potential threat:** HCP audience destination; DocsGPT competes with Site-specific LLM.
- **Information gaps:** Roadmap for AI Ads inside DocsGPT, Pharma marketing product specifics

| Product | Overlap |
|---|---:|
| Marketplace | M |
| ABM | N |
| Premium Programmatic | M |
| RepTwin | M |
| Point-of-Care | N |
| NEXT | L |
| co-pay.com | N |
| Point-of-Dispense | N |

**Registry sources to monitor:**
- Homepage — https://www.doximity.com/ (Homepage; priority 1; Daily; Website crawler; confidence High)
- Press — https://press.doximity.com/ (Newsroom; priority 1; Daily; Sitemap monitor; confidence High)
- Blog — https://blog.doximity.com/ (Blog; priority 2; Weekly; RSS feed; confidence High)
- Investor relations — https://investors.doximity.com/news/default.aspx (Newsroom; priority 1; Daily; Sitemap monitor; confidence High)

## GoodRx

- **Tier:** 2
- **Website:** https://www.goodrx.com/
- **Category:** Consumer prescription savings
- **Short description:** Public company (GDRX). Consumer coupon marketplace; recent expanded access deals (Wegovy HD, Lilly Foundayo).
- **Reason for monitoring:** Doceree co-pay.com explicitly contrasts with GoodRx (inside-EHR vs outside-workflow).
- **Known products:** GoodRx app and website, Coupons, Telehealth
- **Positioning summary:** Leading platform for prescription savings in the US.
- **Potential threat:** Brand-name consumer alternative.
- **Information gaps:** Manufacturer-sponsored deal economics, B2B pharma pipeline

| Product | Overlap |
|---|---:|
| Marketplace | N |
| ABM | N |
| Premium Programmatic | N |
| RepTwin | N |
| Point-of-Care | N |
| NEXT | N |
| co-pay.com | M |
| Point-of-Dispense | L |

**Registry sources to monitor:**
- Press releases — https://investors.goodrx.com/news-and-events/press-releases (Press release; priority 1; Daily; Sitemap monitor; confidence High)

## Hippocratic AI

- **Tier:** 2
- **Website:** https://hippocraticai.com/
- **Category:** Healthcare AI agents (patient-care use cases)
- **Short description:** Safety-focused healthcare LLMs for non-diagnostic patient-facing tasks. 1.8M+ patient calls; 50+ partners across 6 countries; $404M raised.
- **Reason for monitoring:** Adjacent agentic AI; pharma extension would escalate.
- **Known products:** Constellation Architecture multi-LLM safety framework, Patient-facing AI agents
- **Positioning summary:** Building the world's safest generative AI agents for healthcare.
- **Potential threat:** Adjacent agentic AI — pharma rep replacement extension would directly threaten RepTwin.
- **Information gaps:** Pharma commercial-rep extension roadmap

| Product | Overlap |
|---|---:|
| Marketplace | N |
| ABM | N |
| Premium Programmatic | N |
| RepTwin | M |
| Point-of-Care | N |
| NEXT | N |
| co-pay.com | N |
| Point-of-Dispense | N |

**Registry sources to monitor:**
- Homepage — https://hippocraticai.com/ (Homepage; priority 1; Daily; Website crawler; confidence High)
- Press — https://hippocraticai.com/press/ (Press release; priority 1; Daily; Sitemap monitor; confidence High)
- Careers — https://hippocraticai.com/careers/ (Careers; priority 2; Weekly; Website crawler; confidence High)

## IQVIA

- **Tier:** 1
- **Website:** https://www.iqvia.com/
- **Category:** Healthcare data, analytics, technology
- **Short description:** Global life-sciences data + analytics + tech. NPA, NSP, MIDAS, OneKey, E360 RWD; Data Marketplace; OCE; Personalization Hub; AI Assistant; AWS strategic AI collaboration. Owns Lasso.
- **Reason for monitoring:** Largest data + tech competitor across the journey.
- **Known products:** NPA, NSP, MIDAS, OneKey, E360 RWD, Data Marketplace, OCE CRM, Personalization Hub, Next Best Action, IQVIA AI Assistant, AIM XR identity, Lasso
- **Positioning summary:** Transforming Life Sciences with Data, Technology & Human Science.
- **Potential threat:** Data-scale dominance; agentic-AI direction; Lasso-Doceree NEXT head-to-head.
- **Information gaps:** Lasso roadmap post-acquisition, AWS collaboration product implications, AI Assistant feature parity vs RepTwin / NEXT

| Product | Overlap |
|---|---:|
| Marketplace | H |
| ABM | M |
| Premium Programmatic | M |
| RepTwin | L |
| Point-of-Care | M |
| NEXT | H |
| co-pay.com | M |
| Point-of-Dispense | L |

**Registry sources to monitor:**
- Homepage — https://www.iqvia.com/ (Homepage; priority 1; Daily; Website crawler; confidence High)
- Newsroom — https://www.iqvia.com/newsroom (Newsroom; priority 1; Daily; Sitemap monitor; confidence High)
- Reports & Publications — https://www.iqvia.com/insights/the-iqvia-institute/reports-and-publications (Resource center; priority 2; Weekly; Website crawler; confidence High)
- Careers — https://jobs.iqvia.com/ (Careers; priority 2; Weekly; Website crawler; confidence High)

## IQVIA Digital

- **Tier:** 1
- **Website:** https://www.iqviadigital.com/
- **Category:** Omnichannel healthcare marketing and analytics platform; legacy Lasso, now active as IQVIA Digital
- **Short description:** Active label for the former Lasso platform. IQVIA Digital provides healthcare marketing experiences using real-time advanced insights; legacy Lasso operated as an omnichannel healthcare marketing and analytics operating system across programmatic, social, email, endemic and CTV.
- **Reason for monitoring:** Use IQVIA Digital as the active competitor label replacing Lasso; high overlap with NEXT and medium overlap with Premium Programmatic, Marketplace, and POC.
- **Known products:** IQVIA Digital, legacy Lasso omnichannel healthcare marketing platform
- **Positioning summary:** Healthcare marketing operating system (an IQVIA business).
- **Potential threat:** Walled-garden alternative bundled with IQVIA data.
- **Information gaps:** Lasso post-2022 roadmap, Re-branding within IQVIA Digital

| Product | Overlap |
|---|---:|
| Marketplace | M |
| ABM | N |
| Premium Programmatic | M |
| RepTwin | N |
| Point-of-Care | M |
| NEXT | H |
| co-pay.com | N |
| Point-of-Dispense | N |


## Komodo Health

- **Tier:** 2
- **Website:** https://www.komodohealth.com/
- **Category:** Healthcare data; Real-World Data
- **Short description:** Healthcare AI and Real-World Data analytics. Healthcare Map (~325M+ patients); MapLab platform; Marmot AI platform.
- **Reason for monitoring:** Most-named Marketplace competitor; Marmot AI extends overlap to NEXT-adjacent.
- **Known products:** Healthcare Map, MapLab, MapLab Enterprise, MapView, MapExplorer, MapEnhance, Drug Projections, Clinical Alerts, Field Sales Insights, Marmot AI platform
- **Positioning summary:** Healthcare AI & Real-World Data Analytics for Life Sciences.
- **Potential threat:** Marketplace data competitor; Marmot AI threatens NEXT positioning.
- **Information gaps:** Marmot feature parity with NEXT, Pharma campaign-activation roadmap

| Product | Overlap |
|---|---:|
| Marketplace | H |
| ABM | N |
| Premium Programmatic | L |
| RepTwin | N |
| Point-of-Care | L |
| NEXT | M |
| co-pay.com | L |
| Point-of-Dispense | N |

**Registry sources to monitor:**
- Homepage — https://www.komodohealth.com/ (Homepage; priority 1; Daily; Website crawler; confidence High)
- Press — https://www.komodohealth.com/press/ (Newsroom; priority 1; Daily; Sitemap monitor; confidence High)
- Careers — https://www.komodohealth.com/careers/ (Careers; priority 2; Weekly; Website crawler; confidence High)

## Medscape (WebMD Health)

- **Tier:** 1
- **Website:** https://www.medscape.com/
- **Category:** HCP destination; CME; medical news
- **Short description:** Online destination for HCPs. Authenticated NPI data partnership with PulsePoint. Sister to PulsePoint within Internet Brands family.
- **Reason for monitoring:** HCP destination; Authenticated NPI partnership creates multi-product threat.
- **Known products:** Medscape platform, Medscape Extend, CME
- **Positioning summary:** Leading global destination for physicians and HCPs.
- **Potential threat:** HCP destination; Authenticated NPI feeds PulsePoint.
- **Information gaps:** Publisher AI Suite-relevant strategy at Medscape level

| Product | Overlap |
|---|---:|
| Marketplace | M |
| ABM | N |
| Premium Programmatic | M |
| RepTwin | L |
| Point-of-Care | N |
| NEXT | L |
| co-pay.com | N |
| Point-of-Dispense | N |


## OpenEvidence

- **Tier:** 1
- **Website:** https://www.openevidence.com/
- **Category:** Clinical AI for physicians
- **Short description:** AI clinical-decision-support; sources from peer-reviewed publications. Recent $250M raise at $3.5B (Jan 2026). DeepConsult agentic AI.
- **Reason for monitoring:** Doceree's Publisher AI Suite battlecard frames OpenEvidence explicitly as 'the threat'.
- **Known products:** OpenEvidence platform, OpenEvidence DeepConsult
- **Positioning summary:** AI copilot for doctors; clinical decision-making at point of care.
- **Potential threat:** Diverts HCP attention from Doceree publisher network; absorbs AI-era query volume.
- **Information gaps:** Pharma monetization roadmap, DeepConsult enterprise / pharma offerings

| Product | Overlap |
|---|---:|
| Marketplace | N |
| ABM | N |
| Premium Programmatic | L |
| RepTwin | M |
| Point-of-Care | L |
| NEXT | L |
| co-pay.com | N |
| Point-of-Dispense | N |

**Registry sources to monitor:**
- Homepage — https://www.openevidence.com/ (Homepage; priority 1; Daily; Website crawler; confidence High)
- Announcements — https://www.openevidence.com/announcements (Press release; priority 1; Daily; Sitemap monitor; confidence High)

## OptimizeRx

- **Tier:** 1
- **Website:** https://www.optimizerx.com/
- **Category:** Point-of-care marketing; healthcare omnichannel
- **Short description:** Public company. 300+ EHR/ePrescribe partners; DAAP (Dynamic Audience Activation Platform); Micro-Neighborhood Targeting.
- **Reason for monitoring:** Most-named POC competitor; expanding to retail/pharmacy adjacent.
- **Known products:** DAAP, Micro-Neighborhood Targeting, EHR/ePrescribe placements, Patient-chart messaging
- **Positioning summary:** Dynamic, Omnichannel Solutions for Life Sciences Marketing.
- **Potential threat:** Direct head-to-head loss source on POC; DAAP can be misread as orchestration parity with NEXT; pharmacy-adjacent moves overlap with POD.
- **Information gaps:** Match-rate methodology vs Doceree 86-93%, Current pricing, Specific PMS partner names

| Product | Overlap |
|---|---:|
| Marketplace | L |
| ABM | N |
| Premium Programmatic | M |
| RepTwin | L |
| Point-of-Care | H |
| NEXT | M |
| co-pay.com | M |
| Point-of-Dispense | M |

**Registry sources to monitor:**
- Homepage — https://www.optimizerx.com/ (Homepage; priority 1; Daily; Website crawler; confidence High)
- Investor news releases — https://investors.optimizerx.com/news-releases (Press release; priority 1; Daily; Sitemap monitor; confidence High)
- Blog — https://www.optimizerx.com/blog (Blog; priority 2; Weekly; Website crawler; confidence High)
- News & Mentions — https://www.optimizerx.com/news-and-mentions (Newsroom; priority 2; Weekly; Website crawler; confidence High)
- Resources — https://www.optimizerx.com/resources (Resource center; priority 2; Weekly; Website crawler; confidence High)
- Careers — https://www.optimizerx.com/careers (Careers; priority 2; Weekly; Website crawler; confidence High)

## PatientPoint

- **Tier:** 2
- **Website:** https://patientpoint.com/
- **Category:** Owned point-of-care DOOH network
- **Short description:** ~35,000 physician offices; PatientPoint Health Audiences (programmatic).
- **Reason for monitoring:** Largest competing PoC network; programmatic move.
- **Known products:** PatientPoint network, PatientPoint Health Audiences
- **Positioning summary:** The Point of Change Company.
- **Potential threat:** Owned network with programmatic capabilities competes with Spark for DOOH.
- **Information gaps:** Programmatic-buying integration depth

| Product | Overlap |
|---|---:|
| Marketplace | L |
| ABM | N |
| Premium Programmatic | M |
| RepTwin | N |
| Point-of-Care | M |
| NEXT | N |
| co-pay.com | N |
| Point-of-Dispense | N |

**Registry sources to monitor:**
- Newsroom — https://patientpoint.com/news/ (Newsroom; priority 1; Daily; Sitemap monitor; confidence High)

## PulsePoint

- **Tier:** 1
- **Website:** https://www.pulsepoint.com/
- **Category:** Healthcare programmatic; HCP measurement
- **Short description:** Programmatic platform; HCP365 NPI-level measurement; Authenticated NPI with Medscape; Internet Brands / WebMD parent.
- **Reason for monitoring:** Cited across POC, NEXT, and Premium Programmatic battlecards.
- **Known products:** PulsePoint platform, HCP365, Signal Platform, HCP Direct Match, HCP Explorer, Authenticated NPI
- **Positioning summary:** Healthcare Marketing Technology.
- **Potential threat:** Identity-layer competition via Medscape data; programmatic scale; HCP365 measurement.
- **Information gaps:** Match-rate methodology comparison, Depth of EHR middleware integration via Flora

| Product | Overlap |
|---|---:|
| Marketplace | M |
| ABM | N |
| Premium Programmatic | H |
| RepTwin | L |
| Point-of-Care | M |
| NEXT | M |
| co-pay.com | N |
| Point-of-Dispense | N |

**Registry sources to monitor:**
- Homepage — https://www.pulsepoint.com/ (Homepage; priority 1; Daily; Website crawler; confidence High)
- Blog — https://www.pulsepoint.com/blog (Blog; priority 1; Daily; Sitemap monitor; confidence High)
- Press releases — https://www.pulsepoint.com/press-releases (Press release; priority 1; Daily; Sitemap monitor; confidence High)

## RedSail Technologies

- **Tier:** 2
- **Website:** https://www.redsailtechnologies.com/
- **Category:** Pharmacy software (PMS)
- **Short description:** Pharmacy software (PMS) — owns PioneerRx, Axys LTC, QS/1, BestRx, PrimeCare, TransactRx, Emporos, RxMile. ~12,000 pharmacies.
- **Reason for monitoring:** Most-named POD/Spark for Pharmacy competitor — vertical PMS lock-in.
- **Known products:** PioneerRx PMS, Axys LTC, QS/1, BestRx, PrimeCare, TransactRx, Emporos, RxMile, PowerLine
- **Positioning summary:** The Leader in Pharmacy Software and Services.
- **Potential threat:** Vertical lock-in on independents; could expand to chains.
- **Information gaps:** Whether they will open PMS to third-party messaging vendors or pursue exclusive monetization

| Product | Overlap |
|---|---:|
| Marketplace | N |
| ABM | N |
| Premium Programmatic | N |
| RepTwin | N |
| Point-of-Care | N |
| NEXT | N |
| co-pay.com | L |
| Point-of-Dispense | H |

**Registry sources to monitor:**
- Press releases — https://www.redsailtechnologies.com/press-releases (Press release; priority 1; Daily; Sitemap monitor; confidence High)
- News — https://www.redsailtechnologies.com/news (Newsroom; priority 1; Daily; Website crawler; confidence High)

## Relevate Health

- **Tier:** 2
- **Website:** https://www.relevatehealth.com/
- **Category:** Pharma agency-tech hybrid
- **Short description:** ELE Decision Engine; clinically triggered EHR-workflow messages; Level Ex pharma games.
- **Reason for monitoring:** Direct POC competitor; agency-tech bundle.
- **Known products:** ELE Decision Engine, EHR-workflow-triggered messages, Level Ex pharma games
- **Positioning summary:** HCP Omnichannel Marketing & Games.
- **Potential threat:** Direct POC competitor; agency-tech bundle attractive to brands looking for one vendor.
- **Information gaps:** ELE Decision Engine architecture, Specific EHR partners

| Product | Overlap |
|---|---:|
| Marketplace | L |
| ABM | N |
| Premium Programmatic | M |
| RepTwin | N |
| Point-of-Care | H |
| NEXT | M |
| co-pay.com | M |
| Point-of-Dispense | N |


## StackAdapt

- **Tier:** 2
- **Website:** https://www.stackadapt.com/
- **Category:** AI-powered programmatic
- **Short description:** AI-powered programmatic platform across native, display, CTV, video, audio, in-game, DOOH, email. Healthcare suite — NPI Targeting, Script Lift, EHR Inventory.
- **Reason for monitoring:** Cross-vertical DSP with growing healthcare suite; self-serve threat.
- **Known products:** StackAdapt platform, Healthcare suite (NPI Targeting, Script Lift, EHR Inventory)
- **Positioning summary:** The AI-Powered Marketing Platform.
- **Potential threat:** Self-serve programmatic alternative for pharma agencies.
- **Information gaps:** EHR Inventory partner list, Healthcare-specific compliance depth

| Product | Overlap |
|---|---:|
| Marketplace | M |
| ABM | N |
| Premium Programmatic | H |
| RepTwin | N |
| Point-of-Care | L |
| NEXT | M |
| co-pay.com | N |
| Point-of-Dispense | N |

**Registry sources to monitor:**
- Healthcare solution — https://www.stackadapt.com/industry-solutions/healthcare (Solution page; priority 1; Daily; Website crawler; confidence High)

## Swoop

- **Tier:** 2
- **Website:** https://swoop.com/
- **Category:** Predictive HCP / patient audience platform
- **Short description:** HIPAA-certified, NAI-accredited; 300M+ de-identified patients; Swoop Piper. Acquired by W2O Group Sep 2024.
- **Reason for monitoring:** Predictive AI audience play; named in Premium Programmatic and POC battlecards.
- **Known products:** Swoop omnichannel marketing platform, Swoop Piper
- **Positioning summary:** AI-Powered Customer Engagement for Life Sciences.
- **Potential threat:** Predictive audience competition.
- **Information gaps:** Post-W2O roadmap, Pharma activation depth

| Product | Overlap |
|---|---:|
| Marketplace | M |
| ABM | N |
| Premium Programmatic | H |
| RepTwin | L |
| Point-of-Care | M |
| NEXT | M |
| co-pay.com | N |
| Point-of-Dispense | N |


## Trade Desk

- **Tier:** 2
- **Website:** https://www.thetradedesk.com/
- **Category:** Independent omnichannel DSP; pharma marketplace
- **Short description:** Public company (TTD). Leading independent DSP. HCP endemic pharma marketplace launched 2025.
- **Reason for monitoring:** Cross-vertical scale; pharma vertical entry direct competitor; integration partner via BYOP.
- **Known products:** TTD DSP, Sellers and Publishers 500+, OpenPath, HCP endemic pharma marketplace
- **Positioning summary:** Leading independent omnichannel DSP.
- **Potential threat:** Direct Premium Programmatic competitor; also a BYOP integration partner.
- **Information gaps:** Endemic pharma marketplace publisher list, Depth of NPI / context combined targeting

| Product | Overlap |
|---|---:|
| Marketplace | L |
| ABM | N |
| Premium Programmatic | H |
| RepTwin | N |
| Point-of-Care | N |
| NEXT | M |
| co-pay.com | N |
| Point-of-Dispense | N |

**Registry sources to monitor:**
- Press room — https://www.thetradedesk.com/press-room (Newsroom; priority 1; Daily; Sitemap monitor; confidence High)
- Pharma page — https://www.thetradedesk.com/pharma (Solution page; priority 1; Daily; Website crawler; confidence High)

## Veradigm

- **Tier:** 1
- **Website:** https://veradigm.com/
- **Category:** EHR ad media; healthcare data and provider-network tech
- **Short description:** Veradigm Digital Health Media places sponsor messages within prescriber EHR workflows. POCMA-certified. Owns its own EHR ecosystem.
- **Reason for monitoring:** Direct POC competitor; owns competing EHR products.
- **Known products:** Veradigm Digital Health Media, Veradigm Network, Allscripts ambulatory EHRs
- **Positioning summary:** Working together to transform health, insightfully.
- **Potential threat:** Strong incumbent on POC.
- **Information gaps:** Current pricing, Product roadmap post-Allscripts era, Relationship with non-Allscripts EHR vendors

| Product | Overlap |
|---|---:|
| Marketplace | L |
| ABM | N |
| Premium Programmatic | L |
| RepTwin | N |
| Point-of-Care | H |
| NEXT | M |
| co-pay.com | M |
| Point-of-Dispense | N |

**Registry sources to monitor:**
- Homepage — https://veradigm.com/ (Homepage; priority 1; Daily; Website crawler; confidence High)
- Press releases — https://veradigm.com/about-veradigm/press-releases/ (Press release; priority 1; Daily; Sitemap monitor; confidence High)
- In the News — https://veradigm.com/about-veradigm/in-the-news/ (Newsroom; priority 2; Weekly; Website crawler; confidence High)
- Job openings — https://veradigm.com/about-veradigm/careers/job-openings/ (Careers; priority 2; Weekly; Website crawler; confidence High)

# RepTwin Expanded Agentic-AI Competitor Watchlist

This section expands the RepTwin competitor set beyond the original registry. It should be reviewed by Sherry/SME before being promoted to active Day-1 monitoring. The default status for new entries is `needs_validation` or `source_discovery_backlog`, except for highly relevant official sources.

| Competitor | Threat Tier | Why It Matters for RepTwin | Recommended Status | Suggested Sources |
|---|---|---|---|---|
| Synthio Labs | High / direct | Multimodal agentic AI platform purpose-built for pharma workflows; includes Jarvis for field teams, Ather for HCP engagement, Helix for patient support, Simulation Studio and Polaris HQ. | Needs validation / source discovery unless already in registry | https://synthiolabs.com/ |
| Hippocratic AI | Medium / adjacent | Healthcare generative AI agents across provider, payor and pharma; largely patient-facing/non-diagnostic, but pharma category and scale make it an escalation threat if it extends into HCP commercial rep use cases. | Needs validation / source discovery unless already in registry | https://hippocraticai.com/ |
| RoseRx | High / direct | Conversational AI for pharma HCP and patient engagement using approved/MLR content, audit trails, omnichannel intelligence and compliance review. | Needs validation / source discovery unless already in registry | https://www.roserx.ai/ |
| PrescriberPoint / Prescriber.AI | Medium / adjacent | AI-powered point-of-care platform for researching FDA-approved drug/clinical info, understanding coverage/OOP costs, PA, savings enrollment and brand activation. | Needs validation / source discovery unless already in registry | https://business.prescriberpoint.com/ |
| Salesforce Agentforce for Life Sciences | Medium / adjacent | Agentic AI platform for pharma and medtech commercial, clinical and medical engagement at scale; strong platform risk because of CRM footprint. | Needs validation / source discovery unless already in registry | https://www.salesforce.com/life-sciences/artificial-intelligence/ |
| Veeva AI for Vault CRM | Medium / adjacent | Industry-specific AI embedded in Vault CRM; pre-call/voice/field workflow agents strengthen incumbent CRM position. | Needs validation / source discovery unless already in registry | https://www.veeva.com/products/crm-suite/veeva-ai-for-vault-crm/ |
| Aktana / PharmaForceIQ | Medium / adjacent | AI-driven insights, orchestration and decision support for commercial/medical teams; acquired by PharmaForceIQ to create optichannel GTM tech. | Needs validation / source discovery unless already in registry | https://www.aktana.com/ |
| Openhelix | Low / watchlist | AI copilot for life-science reps and managers focused on rep productivity, admin burden, targeting and in-field time. | Needs validation / source discovery unless already in registry | https://www.openhelix.co/ |
| MathCo RepGPT | Low / watchlist | Multi-agent AI framework for pharma sales representatives/MSLs; often services-led but should be monitored for productization. | Needs validation / source discovery unless already in registry | https://mathco.com/article/sales-rep-assistant-repgpt-intelligent-multi-agent-ai-for-pharma-sales-built-on-databricks/ |
| Agilisium Pharma Rep Copilot | Low / watchlist | AI agent / copilot concept for HCP engagement and pharma sales workflows. | Needs validation / source discovery unless already in registry | https://www.agilisium.com/blogs/beyond-traditional-sales-how-ai-agents-are-transforming-hcp-engagement-in-life-sciences |

## RepTwin Competitor Taxonomy

| Category | Description | Examples |
|---|---|---|
| Direct pharma conversational agent | Purpose-built for HCP, field-team, MLR-approved, medical-information, voice/chat/video pharma workflows. | Synthio Labs, RoseRx, PrescriberPoint / Prescriber.AI, PrescriberPoint Engage/REP.AI if verified |
| Adjacent healthcare agent platform | Healthcare AI agents focused on patient, provider, payor, clinical access, or call-center use cases; becomes direct if pharma/HCP commercial workflows expand. | Hippocratic AI, Salesforce Agentforce for Life Sciences, AWS/Connect healthcare agents |
| CRM / life-sciences platform incumbent | Existing CRM/orchestration platforms embedding agents into field or medical workflows. | Veeva AI for Vault CRM, Salesforce Agentforce, IQVIA AI Assistant, Aktana / PharmaForceIQ |
| Field-force copilot / services-led product | AI assistants for sales reps, MSLs, pre-call planning, post-call documentation, training, and productivity. | Openhelix, MathCo RepGPT, Agilisium, Axtria, Indegene, SmartWinnr |
| Medical publisher / HCP destination agent | AI assistants where HCPs ask questions on trusted medical destinations; threatens engagement surface and sponsored interactions. | OpenEvidence, Doximity, Medscape/WebMD, UpToDate |

### RepTwin Escalation Rules

- **Severity 5 candidate:** competitor announces an MLR-approved AI brand rep for pharma with HCP-facing voice/chat/video and brand-trained medical-information workflows.
- **Severity 4 candidate:** competitor announces a pharma HCP agent, field-team AI agent, MSL/FRM agent, or CRM-native commercial agent with evidence of enterprise pharma adoption.
- **Severity 3 candidate:** competitor announces patient-support or call-center healthcare agents with pharma-specific templates or use cases.
- **Severity 2 monitor:** thought leadership, generic agentic-AI claims, or services-led pharma sales assistant without productized HCP engagement evidence.
- **Caveat:** patient-facing AI agents are not direct RepTwin competitors unless evidence shows pharma commercial, HCP engagement, MLR-approved medical-information, or brand-rep use cases.

---
# Source Monitoring and Seed Rules

## Cadence Rules

| Priority | Cadence | Use |
|---:|---|---|
| 1 | Daily | Official product pages, homepages, press releases, newsroom, investor updates, critical category pages. |
| 2 | Weekly | Blogs, careers, resources, secondary solution pages, thought leadership. |
| 3 | Monthly | Older libraries, lower-priority category pages, partner directories, low-confidence sources. |
| 4 | Archive only / manual | Manual-only, gated, unverified, restricted, or backlog sources. |

## Collection Guardrails

- Do not scrape LinkedIn or restricted social platforms. Use approved API/vendor/manual export only.
- Do not automate analyst reports, gated webinars, login walls, paywalls, or CAPTCHA sources.
- Do not invent URLs. If a source is suspected but not verified, mark it `needs_source_discovery`.
- Treat external news as medium confidence unless corroborated by official competitor source.
- Treat job postings as directional; never state them as proof of product launch.
- Store `source_url`, `captured_at`, `source_type`, `collection_method`, `excerpt`, and `confidence` for every evidence item.

---
# Codex-Ready Seed Objects

## Competitor Object

```json
{
  "name": "",
  "aliases": [],
  "tier": "1|2|3|research|post_mvp",
  "website": "",
  "category": "",
  "region": "",
  "primary_doceree_products": [],
  "secondary_doceree_products": [],
  "watchlist_products": [],
  "overlap_matrix": {
    "Marketplace": "H|M|L|N"
  },
  "reason_for_monitoring": "",
  "known_products": [],
  "positioning_summary": "",
  "threat_summary": "",
  "information_gaps": [],
  "source_status": "confirmed|needs_validation|needs_source_discovery",
  "mvp_status": "day1|post_mvp|manual_only|source_discovery_backlog"
}
```

## Product Competitor Mapping Object

```json
{
  "doceree_product": "",
  "competitor": "",
  "overlap_level": "high|medium|low|watchlist",
  "threat_type": "direct|adjacent|platform|data|workflow|publisher|supply_side|agentic_ai|generic_benchmark",
  "why_it_matters": "",
  "buyer_overlap": "",
  "workflow_overlap": "",
  "evidence_strength": "high|medium|low|needs_validation",
  "monitoring_priority": "daily|weekly|monthly|manual|backlog",
  "battlecard_relevant": true,
  "alert_threshold": "severity_3|severity_4|severity_5",
  "source_notes": []
}
```

## Source Discovery Backlog Object

```json
{
  "competitor": "",
  "suspected_source_type": "homepage|product_page|newsroom|press_release|blog|careers|docs|case_study|manual_social|analyst_report",
  "source_description": "",
  "suggested_search_terms": [],
  "doceree_products_impacted": [],
  "priority": "high|medium|low",
  "status": "open|in_review|verified|rejected|archived",
  "assigned_to": "Sherry George",
  "notes": ""
}
```

# Final Competition File Checklist

- [ ] Lasso has been renamed to IQVIA Digital everywhere except historical alias fields.
- [ ] Every Doceree product has direct, adjacent, and watchlist competitor sections.
- [ ] RepTwin includes dedicated agentic-AI competitors: Hippocratic AI, Synthio Labs, RoseRx, PrescriberPoint, Salesforce Agentforce, Veeva AI, Aktana/PharmaForceIQ, Openhelix, MathCo RepGPT, Agilisium, and additional watchlist items.
- [ ] Supply-side products are not forced into demand-side competitor logic.
- [ ] Every competitor can be mapped to a source registry row or source-discovery backlog item.
- [ ] Product mappings include overlap levels and rationales.
- [ ] Monitoring agents are recommended per product.
- [ ] Source governance rules are preserved.
- [ ] Job/social/patent/SEO signals are labeled directional.
- [ ] Codex can convert this file into seed JSON for competitor registry, product-overlap matrix, source-discovery backlog, and battlecard triggers.
---

## Appendix — Codex-Ready Competitor URL Seed Table

Use this table to create `prisma/seeds/data/competitor-urls.seed.json` or to enrich `competitor-sources.seed.json`. Each `key_urls_to_monitor` entry should become one source row only after it passes source-policy validation.

| Canonical Competitor | Official URL | Key URLs to Monitor | Monitoring Notes |
|---|---|---|---|
| 6sense | https://6sense.com/ | https://6sense.com/newsroom/ ; https://6sense.com/product/ ; https://6sense.com/careers/ | Generic B2B ABM/revenue AI platform; healthcare adjacency only. |
| AdButler | https://www.adbutler.com/ | https://www.adbutler.com/display-ad-server/ ; https://help.adbutler.com/ | Ad server and retail media platform. |
| Agilisium Pharma Rep Copilot | https://www.agilisium.com/blogs/beyond-traditional-sales-how-ai-agents-are-transforming-hcp-engagement-in-life-sciences | https://www.agilisium.com/blogs/beyond-traditional-sales-how-ai-agents-are-transforming-hcp-engagement-in-life-sciences ; https://www.agilisium.com/ | Productized services/content around AI agents for pharma HCP engagement. |
| Aktana / PharmaForceIQ | https://pharmaforceiq.com/ | https://www.aktana.com/ ; https://pharmaforceiq.com/pharmaforceiq-acquires-aktana/ | Life sciences commercial/medical AI orchestration; Aktana now under PharmaForceIQ context. |
| AssistRx | https://www.assistrx.com/ | https://www.assistrx.com/specialty-pharmaceutical-solutions/ ; https://www.assistrx.com/specialty-pharmaceutical-solutions/assistrx-patient-solutions/ ; https://www.assistrx.com/careers | Specialty pharma patient access and support services. |
| CCC | https://www.copyright.com/ | https://www.copyright.com/solutions/ ; https://www.copyright.com/news/ | Copyright Clearance Center; content licensing infrastructure. |
| CheckedUp | https://www.checkedup.com/ | https://www.checkedup.com/solutions/ ; https://www.checkedup.com/about-us/ | Point-of-care screens and patient engagement. |
| ConnectiveRx | https://www.connectiverx.com/ | https://www.connectiverx.com/ ; https://www.connectiverx.com/careers ; https://careers-connectiverx.icims.com/jobs/intro?mobile=true&needsRedirect=false | Patient access, copay, hub/support, affordability and adherence. |
| CoverMyMeds | https://www.covermymeds.health/ | https://www.covermymeds.health/our-solutions ; https://www.covermymeds.health/about/newsroom ; https://talentcommunity.mckesson.com/flows/cmm | Medication access, affordability, prior authorization, patient support. |
| Dappier | https://dappier.com/ | https://dappier.com/ ; https://docs.dappier.com/publish-and-monetize | AI content monetization, RAG/answering/copilot monetization for publishers. |
| DeepIntent | https://deepintent.com/ | https://deepintent.com/news ; https://deepintent.com/careers ; https://deepintent.com/solutions | Healthcare DSP, Cortex, Helix, HCP/programmatic activation. |
| DeepIntent via Place Exchange | https://deepintent.com/ | https://www.placeexchange.com/ ; https://deepintent.com/news | Composite tracking for DeepIntent DOOH exposure via Place Exchange. |
| Definitive Healthcare | https://www.definitivehc.com/ | https://www.definitivehc.com/solutions ; https://www.definitivehc.com/blog ; https://www.definitivehc.com/about/careers | Healthcare commercial intelligence, provider/account data. |
| Demandbase | https://www.demandbase.com/ | https://www.demandbase.com/products/account-based-experience/ ; https://www.demandbase.com/about-us/news/ ; https://www.demandbase.com/careers/ | Generic ABM/revenue platform; healthcare adjacency only. |
| Doximity | https://www.doximity.com/ | https://www.doximity.com/marketing-solutions ; https://press.doximity.com/ ; https://www.doximity.com/careers | HCP destination network, marketing solutions, AI/clinical tools, news/press. |
| DrFirst | https://drfirst.com/ | https://drfirst.com/solutions/ ; https://drfirst.com/news/ ; https://drfirst.com/careers/ | e-prescribing, medication management, patient access adjacency. |
| GoodRx | https://www.goodrx.com/ | https://investors.goodrx.com/news-and-events/press-releases ; https://www.goodrx.com/about/careers | Prescription savings, pharma solutions, DTP affordability, investor news. |
| Google Ad Manager | https://admanager.google.com/home/ | https://admanager.google.com/home/ ; https://support.google.com/admanager/ ; https://publishersonair.withgoogle.com/ad-manager-getting-started | Publisher ad management benchmark. |
| Haymarket / M3 / Everyday Health Professional | https://www.haymarketmedia.com/ | https://corporate.m3.com/ ; https://www.everydayhealthgroup.com/ ; https://www.haymarketmedicalnetwork.com/ | Composite HCP/professional media watchlist; validate exact property by market. |
| Hippocratic AI | https://hippocraticai.com/ | https://hippocraticai.com/lifesciences/ ; https://hippocraticai.com/healthcare-agents/ ; https://hippocraticai.com/view-all-agents/ | Healthcare generative AI agents; pharma/life-sciences category watchlist. |
| IQVIA | https://www.iqvia.com/ | https://www.iqvia.com/newsroom ; https://www.iqvia.com/solutions ; https://iqvia.wd1.myworkdayjobs.com/IQVIA/ | Global healthcare data, analytics, clinical/commercial technology; monitor IQVIA.ai, commercial data, digital marketing and AI moves. |
| IQVIA Digital | https://www.iqviadigital.com/ | https://www.iqviadigital.com/solutions ; https://www.iqviadigital.com/resources ; https://www.iqviadigital.com/about-us/careers ; https://www.iqviadigital.com/client-portals | Active label replacing Lasso; monitor solutions/resources/client portals and IQVIA integration. |
| Kevel | https://www.kevel.com/ | https://www.kevel.com/ad-server ; https://dev.kevel.com/reference/getting-started-with-kevel | API ad serving / retail media infrastructure. |
| Komodo Health | https://www.komodohealth.com/ | https://www.komodohealth.com/solutions ; https://www.komodohealth.com/insights ; https://www.komodohealth.com/careers/life-at-komodo/ | Healthcare Map, RWD, analytics, MapLab, AI-enabled life-sciences insights. |
| Magnite | https://www.magnite.com/ | https://www.magnite.com/press/ ; https://www.magnite.com/about-us/ | Independent sell-side advertising platform. |
| MathCo RepGPT | https://mathco.com/article/sales-rep-assistant-repgpt-intelligent-multi-agent-ai-for-pharma-sales-built-on-databricks/ | https://mathco.com/article/sales-rep-assistant-repgpt-intelligent-multi-agent-ai-for-pharma-sales-built-on-databricks/ ; https://mathco.com/ | RepGPT multi-agent pharma sales assistant concept. |
| MedAdvisor | https://www.medadvisor.com/ | https://www.medadvisor.com/ ; https://www.medadvisor.com/news/ | Pharmacy/patient engagement/adherence; validate regional relevance. |
| Medscape (WebMD Health) | https://www.medscapeglobal.com/ | https://www.medscape.com/ ; https://www.webmd.com/mediakit ; https://jobs.jobvite.com/webmd/jobs | Medscape/WebMD professional media and HCP engagement. |
| Medscape / WebMD Health | https://www.medscapeglobal.com/ | https://www.medscape.com/ ; https://www.webmd.com/mediakit ; https://jobs.jobvite.com/webmd/jobs | Same entity grouping as Medscape (WebMD Health). |
| OpenEvidence | https://www.openevidence.com/ | https://www.openevidence.com/ | AI for doctors / clinical evidence; monitor pharma-facing or HCP engagement expansion. |
| Openhelix | https://www.openhelix.co/ | https://www.openhelix.co/ | Healthcare/life sciences AI-agent watchlist. |
| OptimizeRx | https://www.optimizerx.com/ | https://investors.optimizerx.com/news-releases ; https://www.optimizerx.com/blog ; https://www.optimizerx.com/careers | POC/EHR engagement, patient/provider messaging, digital activation, investor news. |
| Outbrain | https://www.outbrain.com/ | https://www.outbrain.com/advertisers/ ; https://www.outbrain.com/blog/ ; https://www.outbrain.com/careers/ | Native/content discovery advertising, adjacent to content marketing. |
| PatientPoint | https://patientpoint.com/ | https://careers.patientpoint.com/ ; https://careers.patientpoint.com/search/searchjobs ; https://patientpoint.com/ | Point-of-care digital screens and patient/HCP engagement network. |
| Place Exchange | https://www.placeexchange.com/ | https://www.placeexchange.com/news ; https://www.placeexchange.com/about | Programmatic OOH exchange; monitor DOOH partnerships. |
| PrescriberPoint | https://prescriberpoint.com/ | https://prescriberpoint.com/prescriber-ai ; https://prescriberpoint.com/insights/introducing-prescriberai ; https://prescriberpointwebapps.com/signup | AI-powered point-of-care prescribing workflow platform; PrescriberAI. |
| PrescriberPoint / Prescriber.AI | https://prescriberpoint.com/ | https://prescriberpoint.com/prescriber-ai ; https://prescriberpoint.com/insights/introducing-prescriberai | Alias grouping for PrescriberPoint and PrescriberAI. |
| PubMatic | https://pubmatic.com/ | https://pubmatic.com/about-us/ ; https://pubmatic.com/news/ ; https://pubmatic.com/solutions/mobile/ | SSP / publisher monetization and AI-powered ad platform. |
| PulsePoint | https://www.pulsepoint.com/ | https://www.pulsepoint.com/resources/newsroom ; https://blog.pulsepoint.com/ ; https://jobs.jobvite.com/pulsepoint/jobs | Healthcare programmatic, HCP365, EHR/programmatic partnerships, WebMD/Internet Brands adjacency. |
| RedSail Technologies | https://www.redsailtechnologies.com/ | https://www.redsailtechnologies.com/press-releases ; https://www.pioneerrx.com/category/press-releases ; https://www.redsailtechnologies.com/careers | Pharmacy management systems; PioneerRx, QS/1, pharmacy network. |
| RedSail Technologies / PioneerRx | https://www.redsailtechnologies.com/ | https://www.pioneerrx.com/ ; https://www.pioneerrx.com/category/press-releases ; https://www.redsailtechnologies.com/press-releases | Use RedSail as parent; PioneerRx as product/brand alias. |
| RelayHealth / Change Healthcare / Optum Insight | https://business.optum.com/en/optum-insight.html | https://www.changehealthcare.com/ ; https://business.optum.com/en/optum-insight.html ; https://www.optum.com/en/about-us/careers.html | Use Optum Insight / Change Healthcare as current grouping; RelayHealth is legacy context. |
| Relevate Health | https://www.relevatehealth.com/ | https://www.relevatehealth.com/news ; https://www.relevatehealth.com/blogs/enhancing-hcp-customer-experience-within-the-ehr-workflow ; https://www.relevatehealth.com/careers | HCP omnichannel campaigns, EHR workflow-triggered messaging, Level Ex games. |
| RoseRx | https://www.roserx.ai/ | https://www.roserx.ai/hcp-engagement-platform ; https://www.roserx.ai/about ; https://www.roserx.ai/contact | AI-powered pharma HCP/patient engagement platform. |
| Salesforce Agentforce for Life Sciences | https://www.salesforce.com/life-sciences/artificial-intelligence/ | https://www.salesforce.com/life-sciences/artificial-intelligence/ ; https://www.salesforce.com/news/ ; https://www.salesforce.com/products/agentforce/ | Platform incumbent; life sciences agentic AI and CRM workflow adjacency. |
| Screenverse | https://www.screenversemedia.com/ | https://www.screenversemedia.com/services/digital-billboards ; https://www.screenversemedia.com/blog | Programmatic DOOH network/monetization. |
| Smaato | https://www.smaato.com/ | https://www.smaato.com/company/ ; https://www.smaato.com/publishers/ ; https://verve.com/brand-marketplace-for-publishers/ | Now framed as Verve Brand+ Marketplace; mobile/omnichannel ad monetization. |
| StackAdapt | https://www.stackadapt.com/ | https://www.stackadapt.com/our-solutions/npi-targeting-and-measurement ; https://www.stackadapt.com/resources ; https://www.stackadapt.com/careers | Programmatic platform with NPI targeting/measurement and healthcare advertising signals. |
| Surescripts | https://surescripts.com/ | https://surescripts.com/solutions ; https://surescripts.com/news-center ; https://surescripts.com/careers | E-prescribing/network infrastructure, benefits, medication history and pharmacy workflow adjacency. |
| Swoop | https://swoop.com/ | https://swoop.com/ ; https://ats.rippling.com/swoopishiring/jobs | AI/data-powered healthcare omnichannel marketing and predictive audiences. |
| Synthio Labs | https://synthiolabs.com/ | https://synthiolabs.com/ | Agentic AI platform for pharma GTM / field, HCP, patient engagement agents. |
| Taboola | https://www.taboola.com/ | https://www.taboola.com/advertisers ; https://www.taboola.com/resources ; https://www.taboola.com/careers | Native/content discovery advertising, adjacent to content marketing. |
| TollBit | https://tollbit.com/ | https://tollbit.com/licensing-platform/ ; https://docs.tollbit.com/docs/monetization | AI content licensing and publisher monetization infrastructure. |
| Trade Desk | https://www.thetradedesk.com/ | https://www.thetradedesk.com/us/solutions ; https://www.thetradedesk.com/us/about-us/newsroom ; https://www.thetradedesk.com/us/careers | Independent DSP; monitor pharma/healthcare marketplace and BYOP integration signals. |
| UpToDate / Wolters Kluwer | https://www.wolterskluwer.com/en/solutions/uptodate | https://www.wolterskluwer.com/en/solutions/uptodate/about ; https://www.uptodate.com/login | Clinical knowledge destination, AI/clinical intelligence watchlist. |
| Veeva AI for Vault CRM | https://www.veeva.com/products/crm-suite/veeva-ai-for-vault-crm/ | https://www.veeva.com/products/crm-suite/veeva-ai-for-vault-crm/ ; https://www.veeva.com/products/crm-suite/ ; https://www.veeva.com/resources | CRM incumbent; Vault CRM AI for life sciences commercial teams. |
| Veeva Crossix | https://www.veeva.com/products/marketing-analytics/ | https://www.veeva.com/products/crossix-data-platform/ ; https://veevacrossix.com/ ; https://www.veeva.com/resources | Marketing analytics, Crossix data platform, patient/HCP measurement. |
| Veradigm | https://veradigm.com/ | https://veradigm.com/about-veradigm/careers/join-our-team/ ; https://veradigm.com/news/ ; https://veradigm.com/solutions/ | EHR, Veradigm Network, Digital Health Media, data/analytics. |
| Vistar Media | https://www.vistarmedia.com/ | https://www.vistarmedia.com/news ; https://www.vistarmedia.com/blog ; https://www.vistarmedia.com/careers | Programmatic DOOH marketplace/platform. |