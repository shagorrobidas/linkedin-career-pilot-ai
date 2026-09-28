"""
Management command to seed realistic demonstration and development data
for LinkedInCareerPilot AI.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import uuid

from accounts.models import User
from tenants.models import Tenant, TenantMember
from profiles.models import UserProfile, Skill, ProfileSnapshot
from jobs.models import Job, JobSkill, JobSource, JobAnalysis
from applications.models import JobApplication, Interview
from content.models import LinkedInPost, PostTopic, PostPerformance
from agents.models import Agent, AgentTask, AgentExecution, AIUsage
from subscriptions.models import Plan, Subscription
from github.models import GitHubRepository, GitHubActivity
from notifications.models import Notification, NotificationPreference
from analytics.models import CareerInsight


class Command(BaseCommand):
    help = 'Seeds realistic development and demo data across all modules'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting LinkedInCareerPilot AI data seeding...'))

        # 1. Demo User
        user, created = User.objects.get_or_create(
            email='demo@linkedincareerpilot.ai',
            defaults={
                'first_name': 'Alex',
                'last_name': 'Rivera',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            }
        )
        user.set_password('Password123!')
        user.first_name = 'Alex'
        user.last_name = 'Rivera'
        user.save()
        self.stdout.write(self.style.SUCCESS(f'✓ User created: {user.email} (password: Password123!)'))

        # 2. Tenant & Membership
        tenant, _ = Tenant.objects.get_or_create(
            slug='alex-rivera-career',
            defaults={
                'name': "Alex Rivera's Career Hub",
                'owner': user,
            }
        )
        tenant_member, _ = TenantMember.objects.get_or_create(
            tenant=tenant,
            user=user,
            defaults={'role': TenantMember.Role.OWNER}
        )
        self.stdout.write(self.style.SUCCESS(f'✓ Tenant created: {tenant.name}'))

        # 3. User Profile
        profile, _ = UserProfile.objects.update_or_create(
            tenant=tenant,
            user=user,
            defaults={
                'headline': 'Staff Software Engineer | Python, Django, React, Cloud & Distributed Systems',
                'about': 'Passionate engineer with 8+ years designing scalable SaaS platforms, event-driven architectures, and high-performance REST APIs. Advocate for automated testing, developer experience, and clean design.',
                'career_focus': 'Senior / Staff Backend & Full-Stack Cloud Engineering',
                'years_of_experience': 8,
                'location': 'San Francisco, CA (Remote)',
                'remote_preference': UserProfile.WorkPreference.REMOTE,
                'desired_salary_min': 150000,
                'desired_salary_currency': 'USD',
                'profile_completion': 92,
            }
        )

        # Profile Skills
        skills_data = [
            ('Python', 8, True),
            ('Django', 7, True),
            ('Django REST Framework', 6, True),
            ('React.js', 5, True),
            ('PostgreSQL', 7, True),
            ('Redis', 5, False),
            ('Docker', 6, False),
            ('Celery', 5, False),
            ('AWS', 4, False),
            ('TypeScript', 4, False),
        ]
        for name, yrs, primary in skills_data:
            Skill.objects.update_or_create(
                profile=profile,
                name=name,
                defaults={'years_of_experience': yrs, 'is_primary': primary}
            )

        # Profile Snapshot
        ProfileSnapshot.objects.update_or_create(
            tenant=tenant,
            profile=profile,
            defaults={
                'overall_health_score': 92,
                'headline_score': 96,
                'about_score': 88,
                'skills_score': 95,
                'projects_score': 92,
                'github_score': 90,
                'suggestions': [
                    'Mention Celery distributed queues directly in your LinkedIn headline.',
                    'Add measurable latency reduction stats to your recent experience description.',
                    'Publish a technical article on Redis caching strategies to boost engagement.'
                ],
                'snapshot_data': {'skills_count': 10, 'profile_views': 340}
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ UserProfile and Skills seeded.'))

        # 4. Job Sources
        src_linkedin, _ = JobSource.objects.get_or_create(name='LinkedIn Jobs', defaults={'provider': 'LinkedIn', 'is_active': True})
        src_remoteok, _ = JobSource.objects.get_or_create(name='RemoteOK', defaults={'provider': 'RemoteOK', 'is_active': True})
        src_yc, _ = JobSource.objects.get_or_create(name='Y Combinator Works', defaults={'provider': 'YC', 'is_active': True})

        # 5. Realistic Curated Jobs & Analyses
        jobs_info = [
            {
                'title': 'Staff Backend Engineer (Distributed Systems)',
                'company': 'CloudScale Global Inc.',
                'location': 'Remote - Worldwide',
                'work_mode': Job.WorkMode.REMOTE,
                'salary_min': 160000,
                'salary_max': 195000,
                'description': 'Seeking an experienced backend architect to scale distributed ingestion pipelines using Python, Django, Celery, and PostgreSQL. Experience with Kubernetes and Redis clustering preferred.',
                'source': src_linkedin,
                'match_score': 96,
                'matched': ['Python', 'Django', 'PostgreSQL', 'Redis', 'Celery', 'Docker'],
                'missing': ['Kubernetes'],
                'rec': 'HIGH_PRIORITY'
            },
            {
                'title': 'Senior Full-Stack Engineer (Python / React)',
                'company': 'FinTech Velocity',
                'location': 'New York, NY (Hybrid)',
                'work_mode': Job.WorkMode.HYBRID,
                'salary_min': 145000,
                'salary_max': 175000,
                'description': 'Build high-security transaction portals. Looking for strong proficiency in Django REST Framework on the backend and React with TypeScript on the frontend.',
                'source': src_yc,
                'match_score': 92,
                'matched': ['Python', 'Django REST Framework', 'React.js', 'PostgreSQL', 'TypeScript'],
                'missing': ['Next.js'],
                'rec': 'HIGH_PRIORITY'
            },
            {
                'title': 'AI Agent Platform Engineer',
                'company': 'Cognitive Engine Labs',
                'location': 'San Francisco, CA (Remote)',
                'work_mode': Job.WorkMode.REMOTE,
                'salary_min': 170000,
                'salary_max': 210000,
                'description': 'Architect autonomous multi-agent execution runtimes. Requires solid Python fundamentals, async task distribution with Celery, and familiarity with LLM orchestration.',
                'source': src_remoteok,
                'match_score': 89,
                'matched': ['Python', 'Celery', 'Docker', 'Redis'],
                'missing': ['vLLM', 'LangChain'],
                'rec': 'HIGH_PRIORITY'
            },
            {
                'title': 'Principal Python & API Architect',
                'company': 'DataStream Systems',
                'location': 'Remote - US / Canada',
                'work_mode': Job.WorkMode.REMOTE,
                'salary_min': 180000,
                'salary_max': 225000,
                'description': 'Lead architectural decisions for enterprise API products. You will mentor teams, optimize high-throughput PostgreSQL schemas, and guide microservice decoupling.',
                'source': src_linkedin,
                'match_score': 94,
                'matched': ['Python', 'Django', 'PostgreSQL', 'AWS', 'Docker'],
                'missing': ['Terraform'],
                'rec': 'HIGH_PRIORITY'
            },
            {
                'title': 'Senior Cloud Backend Engineer (AWS / Python)',
                'company': 'Beacon Health Tech',
                'location': 'Boston, MA (Remote)',
                'work_mode': Job.WorkMode.REMOTE,
                'salary_min': 140000,
                'salary_max': 165000,
                'description': 'Health data synchronization engine. Requires Django or FastAPI, PostgreSQL, HIPAA compliance awareness, and AWS infrastructure experience.',
                'source': src_linkedin,
                'match_score': 87,
                'matched': ['Python', 'Django', 'PostgreSQL', 'AWS'],
                'missing': ['HIPAA', 'FastAPI'],
                'rec': 'MEDIUM_PRIORITY'
            },
            {
                'title': 'Lead React / TypeScript Frontend Architect',
                'company': 'Nova UI Systems',
                'location': 'Remote, North America',
                'work_mode': Job.WorkMode.REMOTE,
                'salary_min': 150000,
                'salary_max': 180000,
                'description': 'Direct our next-generation SaaS frontend design system using React, TypeScript, and modern component architecture.',
                'source': src_yc,
                'match_score': 85,
                'matched': ['React.js', 'TypeScript', 'Docker'],
                'missing': ['GraphQL'],
                'rec': 'MEDIUM_PRIORITY'
            },
        ]

        created_jobs = []
        for jdata in jobs_info:
            job, _ = Job.objects.update_or_create(
                tenant=tenant,
                title=jdata['title'],
                company=jdata['company'],
                defaults={
                    'location': jdata['location'],
                    'work_mode': jdata['work_mode'],
                    'salary_min': jdata['salary_min'],
                    'salary_max': jdata['salary_max'],
                    'currency': 'USD',
                    'description': jdata['description'],
                    'source': jdata['source'],
                    'published_at': timezone.now() - timedelta(days=2),
                }
            )
            created_jobs.append(job)

            # Match Analysis
            JobAnalysis.objects.update_or_create(
                tenant=tenant,
                job=job,
                defaults={
                    'match_score': jdata['match_score'],
                    'matched_skills': jdata['matched'],
                    'missing_skills': jdata['missing'],
                    'experience_compatibility': 'Strong senior level alignment (8 yrs vs 5+ requested)',
                    'career_alignment': 'Direct match with target cloud and backend stack',
                    'recommendation': jdata['rec'],
                    'potential_concerns': ['Requires occasional timezone overlap with PST'],
                }
            )

            # Add Skills
            for skill_name in jdata['matched'] + jdata['missing']:
                JobSkill.objects.get_or_create(
                    job=job,
                    name=skill_name,
                    defaults={'required': True, 'importance': 4}
                )

        self.stdout.write(self.style.SUCCESS(f'✓ {len(created_jobs)} Jobs and AI Analyses seeded.'))

        # 6. Applications
        if len(created_jobs) >= 4:
            apps_data = [
                (created_jobs[0], JobApplication.Status.INTERVIEW, 5, 'Technical Architecture round with VP of Engineering.'),
                (created_jobs[1], JobApplication.Status.APPLIED, 3, 'Application submitted via referral.'),
                (created_jobs[2], JobApplication.Status.SAVED, 1, 'Reviewing culture alignment notes before applying.'),
                (created_jobs[3], JobApplication.Status.OFFER, 14, 'Offer letter received! Reviewing compensation package.'),
            ]
            for job_obj, status_val, days_ago, notes_txt in apps_data:
                app_obj, _ = JobApplication.objects.update_or_create(
                    tenant=tenant,
                    user=user,
                    job=job_obj,
                    defaults={
                        'status': status_val,
                        'applied_date': (timezone.now() - timedelta(days=days_ago)).date(),
                        'notes': notes_txt,
                    }
                )
                if status_val == JobApplication.Status.INTERVIEW:
                    Interview.objects.get_or_create(
                        application=app_obj,
                        stage=Interview.Stage.SYSTEM_DESIGN,
                        defaults={
                            'scheduled_at': timezone.now() + timedelta(days=2),
                            'interviewer_info': 'Sarah Lin (VP Architecture)',
                            'notes': 'Prepare distributed queue and cache invalidation diagram.',
                        }
                    )

        self.stdout.write(self.style.SUCCESS('✓ Job Applications & Interviews seeded.'))

        # 7. LinkedIn Posts
        posts_data = [
            (
                'Django Query Optimization & select_related',
                '🚀 Key insights on tuning Django ORM in high-traffic SaaS:\n\n'
                '1. Use select_related() for single-valued relationships (ForeignKey, OneToOne) to perform SQL JOINs.\n'
                '2. Use prefetch_related() for multi-valued relations (ManyToMany) to batch queries into two fast lookups.\n'
                '3. Always inspect queries with django-debug-toolbar or QuerySet.explain() before deploying.\n\n'
                'Our team reduced endpoint latency from 240ms down to 32ms by eliminating N+1 queries!\n\n'
                '#Django #Python #BackendEngineering #SoftwareArchitecture',
                LinkedInPost.Status.PUBLISHED,
                (4250, 218, 34, 16)
            ),
            (
                'Why Multi-Tenancy Demands Strict Context Isolation',
                'Building multi-tenant applications is about zero-trust data segregation.\n\n'
                'In our architecture, every ORM query resolves tenant context from validated JWT claims — never from client payload bodies.\n\n'
                'Tenant isolation is not an afterthought; it is your baseline security boundary.\n\n'
                '#SaaS #SystemDesign #SoftwareEngineering #CloudSecurity',
                LinkedInPost.Status.PUBLISHED,
                (2890, 145, 22, 9)
            ),
            (
                'Real-Time AI Agents: Managing Execution State with Redis & Celery',
                'When building autonomous agent workflows, synchronous requests simply do not cut it.\n\n'
                'We decouple prompt execution into asynchronous Celery tasks, storing execution milestones in Redis with sub-millisecond status lookups.\n\n'
                'Users get snappy UI feedback with zero thread starvation.\n\n'
                '#AIEngineering #Redis #Celery #Python',
                LinkedInPost.Status.APPROVED,
                (0, 0, 0, 0)
            ),
            (
                '5 Lessons Scaling Django REST APIs to 10k RPS',
                'Draft content covering connection pooling with PgBouncer, response caching with Redis, Gunicorn worker sizing, and database indexing.\n\n'
                '#HighPerformance #Django #RESTAPI #DevOps',
                LinkedInPost.Status.DRAFT,
                (0, 0, 0, 0)
            ),
        ]

        for topic, content, p_status, (imp, react, comm, shr) in posts_data:
            post, _ = LinkedInPost.objects.update_or_create(
                tenant=tenant,
                author=user,
                topic=topic,
                defaults={
                    'content': content,
                    'status': p_status,
                    'ai_generated': True,
                    'human_approved': (p_status in [LinkedInPost.Status.APPROVED, LinkedInPost.Status.PUBLISHED]),
                    'published_at': (timezone.now() - timedelta(days=3)) if p_status == LinkedInPost.Status.PUBLISHED else None,
                }
            )
            if p_status == LinkedInPost.Status.PUBLISHED:
                PostPerformance.objects.update_or_create(
                    post=post,
                    defaults={
                        'impressions': imp,
                        'reactions': react,
                        'comments': comm,
                        'shares': shr,
                        'profile_views_generated': react // 3,
                    }
                )

        self.stdout.write(self.style.SUCCESS('✓ LinkedIn Posts & Performance seeded.'))

        # 8. AI Agents
        agents_data = [
            ('Job Hunter', 'job-hunter', 'Discovers and normalizes high-match tech job opportunities across remote and hybrid boards.', 2),
            ('Job Analyzer', 'job-analyzer', 'Evaluates job descriptions against user resume and skills, extracting missing requirements.', 2),
            ('Content Writer', 'content-writer', 'Generates professional, authentic LinkedIn thought leadership and technical breakdown posts.', 3),
            ('Profile Guardian', 'profile-guardian', 'Audits headline, summary, and experience to identify gaps and boost recruiter search ranking.', 2),
            ('GitHub Monitor', 'github-monitor', 'Scans repositories, releases, and commits to convert code milestones into career narratives.', 1),
            ('Career Analyst', 'career-analyst', 'Synthesizes market demand, skills alignment, and application velocity into weekly guidance.', 3),
        ]
        for name, slug, desc, cost in agents_data:
            Agent.objects.update_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'description': desc,
                    'credit_cost': cost,
                    'is_active': True,
                    'provider': Agent.Provider.GEMINI,
                    'model_name': 'gemini-1.5-pro',
                }
            )
        self.stdout.write(self.style.SUCCESS('✓ AI Agents seeded.'))

        # 9. Subscription Plans & Subscription
        plans_data = [
            ('Free Tier', Plan.PlanType.FREE, 0.00, 0.00, 20, ['Basic Job Search', '1 AI Post / Month', 'Application Tracker']),
            ('Pro Career Pilot', Plan.PlanType.PRO, 29.00, 290.00, 100, ['Unlimited High Match Jobs', 'Daily AI LinkedIn Content', 'Full AI Job Analysis', 'GitHub Career Monitor', '100 AI Credits / Month']),
            ('Executive Growth', Plan.PlanType.PREMIUM, 79.00, 790.00, 300, ['Everything in Pro', 'AI Interview Simulation', 'Automated Recruiter Outreach Drafting', '300 AI Credits / Month', 'Priority Support']),
        ]
        created_plans = []
        for p_name, p_type, price_m, price_y, credits, feats in plans_data:
            plan_obj, _ = Plan.objects.update_or_create(
                plan_type=p_type,
                defaults={
                    'name': p_name,
                    'price_monthly': price_m,
                    'price_yearly': price_y,
                    'ai_credits_monthly': credits,
                    'features': feats,
                    'is_active': True,
                }
            )
            created_plans.append(plan_obj)

        Subscription.objects.update_or_create(
            tenant=tenant,
            defaults={
                'plan': created_plans[1],  # Pro Plan
                'status': Subscription.Status.ACTIVE,
                'ai_credits_remaining': 82,
                'current_period_start': timezone.now() - timedelta(days=10),
                'current_period_end': timezone.now() + timedelta(days=20),
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ Subscription Plans & Active Subscription seeded.'))

        # 10. GitHub Repositories
        repos_data = [
            ('distributed-task-orchestrator', 'Async task orchestration with Redis, Celery, and real-time WebSockets', 'Python', 142, 38),
            ('react-career-copilot', 'Modern dashboard for career tracking with React Router and Tailwind CSS', 'TypeScript', 86, 14),
            ('saas-multi-tenant-starter', 'Django REST Framework starter template with strict tenant isolation', 'Python', 95, 23),
        ]
        for r_name, r_desc, r_lang, stars, forks in repos_data:
            repo, _ = GitHubRepository.objects.update_or_create(
                tenant=tenant,
                full_name=f"alexrivera/{r_name}",
                defaults={
                    'user': user,
                    'repo_name': r_name,
                    'html_url': f"https://github.com/alexrivera/{r_name}",
                    'description': r_desc,
                    'primary_language': r_lang,
                    'languages': {r_lang: 85, 'Shell': 15},
                    'stars_count': stars,
                    'forks_count': forks,
                }
            )

        # 11. Notifications
        Notification.objects.update_or_create(
            tenant=tenant,
            user=user,
            title='High Match Role Discovered',
            defaults={
                'message': 'CloudScale Global Inc. posted "Staff Backend Engineer" with a 96% match for your skills.',
                'notification_type': Notification.NotificationType.HIGH_MATCH_JOB,
                'is_read': False,
            }
        )
        Notification.objects.update_or_create(
            tenant=tenant,
            user=user,
            title='AI Post Draft Ready',
            defaults={
                'message': 'Your AI Agent drafted "Real-Time AI Agents: Managing Execution State with Redis & Celery" for review.',
                'notification_type': Notification.NotificationType.AI_CONTENT_DRAFT,
                'is_read': False,
            }
        )
        Notification.objects.update_or_create(
            tenant=tenant,
            user=user,
            title='Interview Reminder',
            defaults={
                'message': 'System Design interview with CloudScale VP of Architecture in 2 days.',
                'notification_type': Notification.NotificationType.INTERVIEW_REMINDER,
                'is_read': True,
            }
        )
        NotificationPreference.objects.get_or_create(
            user=user,
            defaults={
                'email_enabled': True,
                'telegram_enabled': False,
                'high_match_jobs_notify': True,
                'content_drafts_notify': True,
                'interview_reminders_notify': True,
            }
        )

        # 12. Career Insights
        CareerInsight.objects.update_or_create(
            tenant=tenant,
            title='High Demand for Distributed Systems Knowledge',
            defaults={
                'user': user,
                'category': CareerInsight.InsightCategory.SKILL_GAP,
                'description': '85% of target $160k+ roles request Redis clustering, Celery async tasks, and PostgreSQL query tuning.',
                'actionable_step': 'Publish your scheduled LinkedIn draft explaining Celery distributed architectures to attract inbound recruiters.'
            }
        )
        CareerInsight.objects.update_or_create(
            tenant=tenant,
            title='Top Tier Python & DRF Skill Alignment',
            defaults={
                'user': user,
                'category': CareerInsight.InsightCategory.PROFILE_STRENGTH,
                'description': 'Your match score averages 94% on Python/DRF engineering roles, placing your profile in the top 5% of candidate matches.',
                'actionable_step': 'Keep highlighting your production latency reductions and enterprise SaaS API architectures.'
            }
        )

        self.stdout.write(self.style.SUCCESS(self.style.SUCCESS('\n=========================================')))
        self.stdout.write(self.style.SUCCESS('Successfully seeded all demonstration data!'))
        self.stdout.write(self.style.SUCCESS('Demo User Credentials:'))
        self.stdout.write(self.style.SUCCESS('  Email:    demo@linkedincareerpilot.ai'))
        self.stdout.write(self.style.SUCCESS('  Password: Password123!'))
        self.stdout.write(self.style.SUCCESS('=========================================\n'))
