=======================================================
IIPDash (Integrated Infrastructure Planning Dashboard)
=======================================================

.. image:: https://github.com/tehamalab/iipdash/actions/workflows/pre-commit.yaml/badge.svg
   :target: https://github.com/tehamalab/iipdash/actions/workflows/pre-commit.yaml
   :alt: pre-commit

IIPdash is a **digital infrastructure planning and analysis platform** aiming to improve the
understanding and decision making process related to digital infrastructure with consideration
of social-economic, climate, environment and infrastructure factors.

.. contents:: **Contents**
    :local:


What is the Integrated Infrastructure Planning Platform?
========================================================

This platform helps you explore the potential of an integrated infrastructure planning (IIP) approach to inform investments in digital infrastructure in low- and middle-income countries.
Its goal is to demonstrate the value of IIPs in guiding decisions that serve regional and country development objectives.

*Example: Platform preview*

.. image:: _static/images/iipdash-platform-review.png
   :alt: Dashboard preview


Features
========


**Interactive dashboards for integrated infrastructure planning**

- Explore regional and country-level digital and physical infrastructure through interactive, map-driven dashboards.
- Support a *question-driven* approach to decision-making, helping planners focus on real infrastructure planning needs rather than individual datasets.
- Use predefined *presets* that combine multiple datasets and generate summary statistics to answer common planning questions (eg. how is the schools connectivity).


*Example: Country education dashboard*

.. image:: _static/images/iipdash-schools-connectivity.png
   :alt: Dashboard visualization


**Cross-sectoral data integration in a unified geospatial framework**

- Combine infrastructure, social, economic, environmental and climate risk datasets in a single platform.
- The Climate and environmental layers include flood, drought and cyclone exposure. These layers enable creation of summary statistics on vulnerable communities.
- Enable analysis to reflect the reality that infrastructure planning questions span multiple data domains.

*Example: Vulnerable communities*

.. image:: _static/images/iipdash-vulnerable-communities.png
   :alt: Vulnerable communities


**Geospatial analytics across the infrastructure lifecycle**

- Support infrastructure *design*, *implementation* and *monitoring & evaluation (M&E)* using geospatial analytics.
- Identify opportunities for energy, digital deployment and identify locations for climate risk hotspots during planning.
- Evaluate outcomes to understand whether infrastructure investments improve connectivity, resilience and community outcomes.

*Example: Gaps in digital access*

.. image:: _static/images/iipdash-gaps-access.png
    :alt: Gaps access


**Advanced spatial analysis and GIS-based visualization**

- Visualize infrastructure and risk in geographic context using maps, overlays, filters and spatial queries.
- Measure accessibility, proximity (e.g. distance to fiber) and exposure to hazards.
- Dynamically filter datasets by infrastructure type, socio-economic indicators or selected hazards.
- Access maps, charts and summary statistics for reporting and policy discussions.

**Web-based, open-source and customizable platform**

- Access the platform through a modern web browser with no local installation required.
- Open-source architecture allows full customization to meet organizational and country-specific needs (e.g. data sources, presets, workflows).
- Designed for integration with existing GIS and planning tools used by institutions, this can be achieved through the provided API and documentation
  that faciliate smooth functionality discovery and integration with other tools.

**Designed to support institutional adoption and collaboration**

- Intended as an illustrative prototype demonstrating what is possible with integrated geospatial analytics.
- Can be repurposed, extended and operationalized.
- Supports collaboration among planners, GIS specialists, data managers and decision-makers.


Data Sources & Licensing
=======================

- Most data layers are **publicly available**, while some are licensed.
- Selecting a layer in the Home view provides metadata on **source, recency and coverage**.
- Raw data has usually been minimally processed (cleaning or restructuring) for integration into IIPDash.
- Summary statistics displayed on the platform are **pre-calculated by the World Bank**. Full-scale deployments could perform similar calculations in real time.
- The platform source code is released under the **MIT/GPL open-source license**, enabling adaptation and reuse.


Who Is IIPDash For?
==================

- Government agencies planning digital infrastructure.
- International development organizations seeking evidence-based insights.
- Researchers and analysts in infrastructure, economics, or environmental planning.
- NGOs and private sector partners supporting regional development initiatives.


Why IIPDash Matters
===================

- Helps align infrastructure investments with national and regional development objectives.
- Supports decision-making with clear, visual and interactive insights.
- Encourages integrated planning by considering multiple sectors simultaneously.


**Prototype scope:**  
As a prototype covering three countries, it is limited by the quality and recency of the available data.
While all efforts have been made to ensure accurate data, some features and datasets may be incomplete or missing.


Implementation Overview
=======================

IIPDash is built on reliable, open-source technologies:

- **Django** for the web application framework.
- **PostgreSQL/PostGIS** for spatial and relational data storage.
- **Celery** and **Redis** for background processing and asynchronous tasks.


Installation
============

Information about installation, development and deployment can be found here :doc:`/installation`.


Documentation
=============
A range of documentation is available see :doc:`/admin_guide` for the admin documentation 
and `API link<http://digitalinfraplanning.org/openapi/docs>`__ for API docs.


Contribution Guidelines
=======================
See :doc:`/contributing` for the contributing guidelines for this project.


