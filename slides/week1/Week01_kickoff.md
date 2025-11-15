# Week 1: Kickoff, AWS/S3, Vacoreum, Team Formation

**Title**: CSE255: Scalable Data Analysis with Dask  
**Subtitle**: Week 1: Kickoff, AWS/S3, Vacoreum, Team Formation  
**Author**: Course Instructor

---

## Slide 1: Title Page

---

## Slide 2: Course Overview

- **Format**: 10 weeks; 3 × 50-minute lectures;
- **Teams**: 5 students/team; each team selects a public dataset
- **Grading**: 5 HW focused on the analysis of airline delay dataset
- **Focus**: AWS/S3/Cursor stack, Dask, visualization, PCA, Genaralized additive models, XGBoost, hypothesis-driven modeling

---

## Slide 3: Learning Objectives

- Understand course scope, evaluation, and example questions
- Set up AWS accounts and understand IAM basics
- Organize S3 buckets and understand data access patterns
- Understand cost management

---

## Slide 4: Course Scope

### What We'll Cover
- AWS/S3 infrastructure with cost management
- Dask for scalable analytics
- Visualization through figures, geospatial visualization
- statistical models: PCA, Splines, generalized Additive Models, Boosting
- Statistical inference and hypothesis testing

### What You'll Build
Statistical models that explain the causes for flight delays.

---

## Slide 5: Example Questions

**Example Domain Questions:**
- What are the main causes of flight delays
- Are there correlations between flight delays?
- What are the historical trends of flight delays?

**Technical Questions:**
- How can we use samples of the data effectively?
- How to partition data efficiently?
- How to verify that our analysis is correct?

---

## Slide 6: AWS Account Setup

- Create AWS account (if needed)
- Set up IAM users and roles
- Enable MFA for security
- Set up billing alerts

### IAM Basics
- Users: individual access
- Groups: collections of users
- Roles: temporary permissions
- Policies: define permissions

---

## Slide 7: S3 Organization

### Bucket Structure
- `s3://team-name-project/`
  - `raw/` --- original data
  - `bronze/` --- initial Parquet
  - `silver/` --- cleaned, validated
  - `results/` --- analysis outputs

### Best Practices
- Use versioning for important data
- Enable lifecycle policies
- Use tags for cost tracking
- Set appropriate access policies

---

## Slide 8: Dataset Selection Criteria

- **Size**: Prefer ≥3 GB, not more than 6GB
- **Access**: Public, stable access
- **License**: Permissible for academic use
- **Potential**: Clear geospatial or temporal aggregation

### Good Examples
- NYC TLC trips
- OpenAQ air quality
- OpenStreetMap extracts
- NOAA water data
- GDELT, Yelp, Common Crawl subsets

### Not Allowed
Instructor's weather dataset (reserved for demos)

---

## Slide 9: Vacoreum Cost Management

### Setup Steps
1. Link AWS account to Vacoreum
2. Create budget for the project
3. Set up alert policies
4. Configure tagging strategy

### What to Monitor
- Daily spend trends
- Cost per service (EC2, S3, etc.)
- Cost per 1M rows ingested
- Storage footprint

---

## Slide 10: Week 1 Deliverables

### Project Proposal (1-2 pages)
- Dataset description and access plan
- Initial research questions
- Identified risks and mitigation

### Repository Setup
- Initialize repo with `environment.yml`
- Create `README.md`
- Define team roles
- Document tagging policy

### Vacoreum Evidence
Screenshot: linked account, active budget, alert policy

---

## Slide 11: Homework 1 (5%)

### AWS/S3 Setup Validation
- Create S3 bucket and upload sample data
- Verify IAM permissions
- Test data fetch from S3 using Python

### Cost Hygiene Checklist
- Billing alerts configured
- Vacoreum budget active
- Tagging strategy documented

### Vacoreum Alert Test
Trigger a test alert to verify notification system

---

## Slide 12: Team Formation

### Suggested Roles
- Data Engineer
- Infra/DevOps
- Visualization Lead
- Modeling Lead
- QA/Validation
- PM/Documentation
- Research/Reading
- **Cost & Governance Lead** --- Vacoreum dashboards, tagging compliance

### Process
- Weekly stand-ups with progress notes
- GitHub Projects for task tracking
- PR reviews required

---

## Slide 13: Technology Stack

### Core Packages
- `dask[complete]`, `distributed`
- `pandas`, `pyarrow`, `s3fs`
- `bokeh`, `matplotlib`, `plotly`

### ML/Stats
- `dask-ml`, `scikit-learn`, `xarray`
- `statsmodels`, `pygam`

### Visualization
`ipyleaflet` for geospatial maps

---

## Slide 14: Key Principles

### Parquet is Canonical
All data should be stored in Parquet format

### S3 URIs for Data Access
Use S3 URIs consistently: `s3://bucket/path/to/file.parquet`

### Cost Awareness
Monitor and optimize costs from day one

### Reproducibility
All code must be runnable via `make` or single entrypoint

---

## Slide 15: Next Steps

1. Form teams and assign roles
2. Select dataset and write proposal
3. Set up AWS account and S3 buckets
4. Configure Vacoreum
5. Initialize repository
6. Complete HW1

### Questions?
Office hours: [TBD]  
Slack: [TBD]

