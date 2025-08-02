from .base_agent import BaseAgent, Task, AgentOutput, Priority, TaskStatus
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime

@dataclass
class UserStory:
    id: str
    title: str
    description: str
    acceptance_criteria: List[str]
    priority: Priority
    story_points: int
    user_persona: str
    business_value: str

@dataclass
class ProductRequirement:
    feature_name: str
    description: str
    user_stories: List[UserStory]
    success_metrics: List[str]
    assumptions: List[str]
    constraints: List[str]
    dependencies: List[str]
    timeline: str
    budget_estimate: Optional[str] = None

@dataclass
class PMHandoff:
    project_name: str
    requirements: ProductRequirement
    technical_considerations: List[str]
    risk_assessment: List[Dict[str, str]]
    stakeholder_map: Dict[str, str]
    communication_plan: Dict[str, Any]
    definition_of_done: List[str]

class ProductManagerAgent(BaseAgent):
    def __init__(self, name: str = "PM Agent"):
        super().__init__(name, "Product Manager")
        
    def validate_input(self, task: Task) -> bool:
        required_fields = ['problem_statement', 'target_users', 'business_goals']
        return all(field in task.metadata for field in required_fields)
    
    def process_task(self, task: Task) -> AgentOutput:
        if not self.validate_input(task):
            return AgentOutput(
                agent_role=self.role,
                task_id=task.id,
                content={"error": "Missing required fields: problem_statement, target_users, business_goals"},
                status="failed"
            )
        
        # Extract user stories from problem statement
        user_stories = self._extract_user_stories(task)
        
        # Create product requirements
        requirements = self._create_requirements(task, user_stories)
        
        # Perform stakeholder analysis
        stakeholder_map = self._analyze_stakeholders(task)
        
        # Assess risks
        risks = self._assess_risks(task, requirements)
        
        # Create handoff document
        handoff = PMHandoff(
            project_name=task.title,
            requirements=requirements,
            technical_considerations=self._identify_technical_considerations(requirements),
            risk_assessment=risks,
            stakeholder_map=stakeholder_map,
            communication_plan=self._create_communication_plan(),
            definition_of_done=self._define_done_criteria(requirements)
        )
        
        return AgentOutput(
            agent_role=self.role,
            task_id=task.id,
            content={
                "handoff_document": handoff,  # Let the JSON serializer handle this
                "next_steps": self._define_next_steps(),
                "questions_for_eng": self._generate_engineering_questions(requirements)
            },
            next_agent="Engineering Manager",
            artifacts=[
                {"type": "requirements_doc", "content": requirements},
                {"type": "user_stories", "content": user_stories},
                {"type": "risk_matrix", "content": risks}
            ]
        )
    
    def _extract_user_stories(self, task: Task) -> List[UserStory]:
        problem = task.metadata.get('problem_statement', '')
        target_users = task.metadata.get('target_users', [])
        
        # This would typically use LLM to extract stories from problem statement
        # For demo, creating sample stories based on music events app
        if 'music' in problem.lower() and 'event' in problem.lower():
            return [
                UserStory(
                    id="US-001",
                    title="Discover Local Music Events",
                    description="As a music fan, I want to discover local music events so that I can attend concerts I'm interested in",
                    acceptance_criteria=[
                        "User can search events by location",
                        "User can filter by music genre",
                        "User can see event details (date, venue, price)",
                        "User can save events to favorites"
                    ],
                    priority=Priority.HIGH,
                    story_points=8,
                    user_persona="Music Enthusiast",
                    business_value="Core feature for user acquisition"
                ),
                UserStory(
                    id="US-002",
                    title="Purchase Tickets",
                    description="As a music fan, I want to purchase tickets through the app so that I can secure my attendance",
                    acceptance_criteria=[
                        "User can select ticket quantities",
                        "User can complete secure payment",
                        "User receives confirmation email",
                        "User can access digital tickets"
                    ],
                    priority=Priority.HIGH,
                    story_points=13,
                    user_persona="Music Enthusiast",
                    business_value="Primary revenue stream"
                ),
                UserStory(
                    id="US-003",
                    title="Event Recommendations",
                    description="As a music fan, I want personalized event recommendations so that I can discover new artists and events",
                    acceptance_criteria=[
                        "System tracks user music preferences",
                        "System suggests events based on listening history",
                        "User can rate recommendations",
                        "Recommendations improve over time"
                    ],
                    priority=Priority.MEDIUM,
                    story_points=21,
                    user_persona="Music Enthusiast",
                    business_value="User engagement and retention"
                )
            ]
        return []
    
    def _create_requirements(self, task: Task, user_stories: List[UserStory]) -> ProductRequirement:
        return ProductRequirement(
            feature_name=task.title,
            description=task.description,
            user_stories=user_stories,
            success_metrics=[
                "User acquisition rate > 1000/month",
                "User retention rate > 70% after 30 days",
                "Ticket conversion rate > 15%",
                "Average session duration > 5 minutes"
            ],
            assumptions=[
                "Users have smartphones with internet access",
                "Local venues will partner for event listings",
                "Payment processing integration available",
                "Music streaming data accessible for recommendations"
            ],
            constraints=[
                "Must comply with ticket resale regulations",
                "Payment processing fees < 3%",
                "App size < 100MB",
                "Support iOS 14+ and Android 8+"
            ],
            dependencies=[
                "Venue partnership agreements",
                "Payment gateway integration",
                "Music data API access",
                "Push notification service"
            ],
            timeline="MVP in 3 months, full feature set in 6 months"
        )
    
    def _analyze_stakeholders(self, task: Task) -> Dict[str, str]:
        return {
            "Primary Users": "Music fans aged 18-35 in urban areas",
            "Business Stakeholders": "CEO, VP Product, Marketing Director",
            "Technical Stakeholders": "CTO, Lead Engineers, DevOps",
            "External Partners": "Venues, ticketing platforms, payment processors",
            "Regulatory": "Consumer protection agencies, data privacy officers"
        }
    
    def _assess_risks(self, task: Task, requirements: ProductRequirement) -> List[Dict[str, str]]:
        return [
            {
                "risk": "Low venue adoption",
                "impact": "High",
                "probability": "Medium",
                "mitigation": "Start with major venues, offer revenue sharing"
            },
            {
                "risk": "Payment security breach",
                "impact": "Critical",
                "probability": "Low",
                "mitigation": "Use established payment processors, regular security audits"
            },
            {
                "risk": "Competition from established players",
                "impact": "High",
                "probability": "High",
                "mitigation": "Focus on superior UX and local market expertise"
            },
            {
                "risk": "Scalability issues during high-demand events",
                "impact": "High",
                "probability": "Medium",
                "mitigation": "Load testing, cloud auto-scaling, queue management"
            }
        ]
    
    def _identify_technical_considerations(self, requirements: ProductRequirement) -> List[str]:
        return [
            "Real-time inventory management for ticket sales",
            "Geographic search and mapping integration",
            "Secure payment processing with PCI compliance",
            "Push notification system for event updates",
            "Recommendation engine with ML capabilities",
            "Image/media optimization for event listings",
            "Offline capability for purchased tickets",
            "Analytics and tracking integration"
        ]
    
    def _create_communication_plan(self) -> Dict[str, Any]:
        return {
            "stakeholder_updates": "Weekly status reports to business stakeholders",
            "user_feedback": "Bi-weekly user research sessions",
            "development_sync": "Daily standups with engineering team",
            "risk_escalation": "Immediate notification for high-impact risks",
            "launch_communication": "Multi-channel launch campaign plan"
        }
    
    def _define_done_criteria(self, requirements: ProductRequirement) -> List[str]:
        return [
            "All user stories meet acceptance criteria",
            "Performance benchmarks achieved (page load < 2s)",
            "Security audit passed",
            "Accessibility compliance (WCAG 2.1 AA)",
            "Cross-platform testing completed",
            "Analytics tracking implemented",
            "Documentation completed",
            "Stakeholder sign-off received"
        ]
    
    def _define_next_steps(self) -> List[str]:
        return [
            "Engineering Manager to review technical feasibility",
            "Architecture design session with tech leads",
            "UI/UX design kickoff meeting",
            "Vendor evaluation for payment processing",
            "Legal review of terms and privacy policy",
            "Marketing strategy alignment session"
        ]
    
    def _generate_engineering_questions(self, requirements: ProductRequirement) -> List[str]:
        return [
            "What's the expected concurrent user load for ticket sales?",
            "Which payment processors should we integrate with?",
            "What's the preferred approach for real-time event updates?",
            "Should we build native apps or use cross-platform framework?",
            "What data retention policies need to be implemented?",
            "How should we handle partial payment failures?",
            "What's the backup plan if primary APIs go down?",
            "Should recommendation engine be built in-house or use third-party?"
        ]