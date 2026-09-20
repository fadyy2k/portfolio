# Fady Mounir Zaghloul — Engineering Portfolio

[![Portfolio Quality](https://github.com/fadyy2k/portfolio/actions/workflows/quality.yml/badge.svg)](https://github.com/fadyy2k/portfolio/actions/workflows/quality.yml)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-2ea44f?logo=githubpages)](https://fadyy2k.github.io/portfolio/)

Interactive engineering portfolio focused on **infrastructure, platform engineering, DevOps, cybersecurity, cloud architecture, and production operations**.

## Highlights

- Animated engineering-first hero and infrastructure flow
- Featured public engineering labs with direct architecture/repository links
- Sanitized production case studies separated from client/freelance work
- Career history, technical skills, certifications, and education
- Responsive mobile navigation and reduced-motion support
- GitHub, LinkedIn, Credly, and contact integration
- Open Graph/Twitter social preview metadata and JSON-LD person schema
- Favicon, `robots.txt`, and `sitemap.xml`
- Automated static quality checks plus native GitHub Pages deployment from `main`

## Featured Engineering

- [Platform Engineering — AWS EKS GitOps](https://github.com/fadyy2k/platform-engineering-eks-gitops)
- [MIND DevSecOps Platform](https://github.com/fadyy2k/depi-mind-app-v2)
- [AWS EKS Infrastructure v2](https://github.com/fadyy2k/depi-helloapp-infra-v2)
- [Multi-EC2 Ansible Automation](https://github.com/fadyy2k/notesapp-multi-ec2-ansible)

## Local Preview

```bash
python -m http.server 8000
```

Open `http://localhost:8000`.

Run the structural checks with:

```bash
python scripts/check_site.py
```

## Deployment

GitHub Actions publishes the repository to:

**https://fadyy2k.github.io/portfolio/**

## Security

This is a public portfolio. Production endpoints, credentials, customer/company data, private network details, and authenticated operational screenshots must not be committed.

## License

MIT
