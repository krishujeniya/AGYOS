---
name: devops-career-roadmap
description: Turn the supplied 30-week DevOps Roadmap by belikeanu into a paced learning plan, project sequence, or portfolio checklist. Use for DevOps beginner roadmaps covering Linux, networking, Git, scripting, Docker, CI/CD, AWS, Terraform, Ansible, Kubernetes, Argo CD, monitoring, logging, security, and job preparation.
metadata:
  origin: user-supplied-reference
---

# DevOps career roadmap

Use the supplied roadmap as a sequence of topics and practice projects, not a promise of job readiness after a fixed number of weeks.

## Workflow

1. Read `docs/references/industry/DevOps-Roadmap-belikeanu.txt`; use the PDF beside it as the source copy.
2. Ask about current experience, available hours, operating system, budget, and target role. Preserve topic order where prerequisites matter, then adjust the weekly pace.
3. Organize work in the source's five phases: foundations (weeks 1–8), containers and delivery (9–14), infrastructure and orchestration (15–22), monitoring and security (23–25), and portfolio/job search (26–30).
4. Keep a hands-on deliverable for each topic. The source lists Linux, networking, Git/GitHub, scripting, Docker, CI/CD, AWS, Terraform, Ansible, Kubernetes, Argo CD, metrics, logs, and security basics.
5. Sequence the four portfolio projects from the source: static site on AWS with Terraform and GitHub Actions; app stack with Docker Compose; Kubernetes app with Helm, Argo CD, and Grafana; then a full test/build/scan/deploy/alert pipeline.
6. Add cost controls before any cloud exercise: billing alert, least-privilege credentials, budget limits, and a clear teardown checklist. Do not provision or destroy resources without explicit approval.
7. Treat certification choices, exam prices, cloud free tiers, versions, and hiring practices as time-sensitive. Verify current primary sources before advising.
8. Track evidence by project: problem, architecture diagram, repository, screenshots, security checks, cost, and what the learner can explain in an interview.

## Limits

The roadmap is a curriculum outline, not a hiring guarantee. Do not promise employment or present certificates as substitutes for working projects. Follow AGYOS CI-only rules for this repository: all tests, builds, infrastructure checks, and deployments belong in GitHub Actions or an explicitly authorized target workflow.
