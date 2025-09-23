"""
Slack Mock API
AI-optimized team communication and incident coordination
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from faker import Faker

fake = Faker()

class SlackMock:
    """Mock Slack API for AI-powered incident communication"""
    
    def __init__(self):
        self.channels = {
            "#incidents": {"id": "C1234567890", "members": 25, "purpose": "Incident response coordination"},
            "#alerts": {"id": "C2345678901", "members": 15, "purpose": "System alerts and monitoring"},
            "#devops": {"id": "C3456789012", "members": 12, "purpose": "DevOps team discussions"},
            "#engineering": {"id": "C4567890123", "members": 50, "purpose": "Engineering team updates"},
            "#on-call": {"id": "C5678901234", "members": 8, "purpose": "On-call engineer coordination"}
        }
        
        self.users = [
            {"id": "U1234567890", "name": "alice.engineer", "real_name": "Alice Engineer", "is_online": True},
            {"id": "U2345678901", "name": "bob.devops", "real_name": "Bob DevOps", "is_online": True},
            {"id": "U3456789012", "name": "charlie.sre", "real_name": "Charlie SRE", "is_online": False},
            {"id": "U4567890123", "name": "diana.oncall", "real_name": "Diana OnCall", "is_online": True},
            {"id": "U5678901234", "name": "eve.manager", "real_name": "Eve Manager", "is_online": True}
        ]
        
        self.message_history = []
        self.incident_channels = {}
    
    def send_notification(self, channel: str, message: str, severity: str = "info") -> Dict[str, Any]:
        """Send AI-generated notifications with rich formatting"""
        
        # Ensure channel starts with #
        if not channel.startswith("#"):
            channel = f"#{channel}"
        
        # Get or create channel info
        channel_info = self.channels.get(channel, {
            "id": f"C{random.randint(1000000000, 9999999999)}",
            "members": random.randint(5, 30),
            "purpose": "AI-generated channel"
        })
        
        # Generate message ID and timestamp
        message_id = f"msg_{random.randint(1000000000, 9999999999)}"
        timestamp = datetime.now().isoformat()
        
        # Create rich message formatting based on severity
        formatted_message = self._format_message_by_severity(message, severity)
        
        # Generate AI-enhanced message metadata
        ai_metadata = {
            "confidence": random.uniform(0.8, 0.95),
            "urgency_score": self._calculate_urgency_score(severity, message),
            "audience_targeting": self._analyze_audience_targeting(channel, message),
            "follow_up_recommended": self._should_recommend_follow_up(severity, message),
            "escalation_suggested": severity in ["high", "critical", "P0", "P1"]
        }
        
        # Store message in history
        message_record = {
            "id": message_id,
            "channel": channel,
            "channel_id": channel_info["id"],
            "text": message,
            "formatted_text": formatted_message,
            "severity": severity,
            "timestamp": timestamp,
            "user": "AI-System",
            "user_id": "U_AI_SYSTEM",
            "ai_metadata": ai_metadata,
            "reactions": self._generate_realistic_reactions(severity),
            "thread_ts": None,
            "reply_count": 0
        }
        
        self.message_history.append(message_record)
        
        # Simulate delivery confirmation
        delivery_status = {
            "ok": True,
            "channel": channel_info["id"],
            "ts": f"{int(datetime.now().timestamp())}.{random.randint(100000, 999999)}",
            "message": {
                "type": "message",
                "subtype": "bot_message",
                "text": formatted_message,
                "ts": f"{int(datetime.now().timestamp())}.{random.randint(100000, 999999)}",
                "username": "AI Incident Bot",
                "bot_id": "B_AI_INCIDENT_BOT",
                "attachments": self._generate_message_attachments(severity, message)
            },
            "ai_delivery_metrics": {
                "delivery_time_ms": random.randint(50, 200),
                "estimated_reach": channel_info["members"],
                "expected_response_time": self._estimate_response_time(severity, channel),
                "notification_effectiveness": random.uniform(0.75, 0.95)
            }
        }
        
        return delivery_status
    
    def create_incident_channel(self, incident_id: str) -> Dict[str, Any]:
        """Create incident-specific channel for AI coordination"""
        
        channel_name = f"incident-{incident_id.lower()}"
        channel_id = f"C{random.randint(1000000000, 9999999999)}"
        
        # Generate channel metadata
        channel_info = {
            "id": channel_id,
            "name": channel_name,
            "is_channel": True,
            "is_group": False,
            "is_im": False,
            "created": int(datetime.now().timestamp()),
            "creator": "U_AI_SYSTEM",
            "is_archived": False,
            "is_general": False,
            "unlinked": 0,
            "name_normalized": channel_name,
            "is_shared": False,
            "is_ext_shared": False,
            "is_org_shared": False,
            "pending_shared": [],
            "is_pending_ext_shared": False,
            "is_member": True,
            "is_private": False,
            "is_mpim": False,
            "topic": {
                "value": f"Incident response for {incident_id}",
                "creator": "U_AI_SYSTEM",
                "last_set": int(datetime.now().timestamp())
            },
            "purpose": {
                "value": f"Coordinating response for incident {incident_id}. AI-managed incident channel.",
                "creator": "U_AI_SYSTEM",
                "last_set": int(datetime.now().timestamp())
            },
            "num_members": 0
        }
        
        # Store incident channel
        self.incident_channels[incident_id] = channel_info
        self.channels[f"#{channel_name}"] = {
            "id": channel_id,
            "members": 0,
            "purpose": f"Incident {incident_id} coordination"
        }
        
        # Generate AI recommendations for channel setup
        ai_recommendations = {
            "suggested_members": self._get_suggested_incident_members(incident_id),
            "recommended_integrations": [
                "PagerDuty incident updates",
                "Monitoring alerts feed",
                "Status page updates",
                "Jira ticket integration"
            ],
            "communication_strategy": self._generate_communication_strategy(incident_id),
            "escalation_plan": self._generate_escalation_plan(incident_id)
        }
        
        # Send initial setup message
        setup_message = f"""🚨 **Incident Response Channel Created**
        
**Incident ID:** {incident_id}
**Channel:** #{channel_name}
**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**AI Recommendations:**
• Invite key responders: {', '.join(ai_recommendations['suggested_members'][:3])}
• Enable monitoring integrations
• Set up status updates automation

**Next Steps:**
1. Assess incident severity and impact
2. Assign incident commander
3. Begin coordinated response
        """
        
        # Send setup message to the new channel
        self.send_notification(f"#{channel_name}", setup_message, "high")
        
        return {
            "ok": True,
            "channel": channel_info,
            "ai_setup": {
                "incident_id": incident_id,
                "channel_name": channel_name,
                "channel_id": channel_id,
                "setup_complete": True,
                "recommendations": ai_recommendations,
                "estimated_response_team_size": len(ai_recommendations["suggested_members"]),
                "coordination_confidence": random.uniform(0.85, 0.95)
            },
            "automation_features": {
                "auto_updates_enabled": True,
                "ai_moderation": True,
                "smart_notifications": True,
                "escalation_triggers": True
            }
        }
    
    def get_channel_history(self, channel: str, limit: int = 50) -> Dict[str, Any]:
        """Get channel message history for AI analysis"""
        
        # Filter messages for the specified channel
        channel_messages = [
            msg for msg in self.message_history 
            if msg["channel"] == channel
        ][-limit:]
        
        return {
            "ok": True,
            "messages": channel_messages,
            "has_more": len(self.message_history) > limit,
            "pin_count": random.randint(0, 5),
            "channel_analysis": {
                "total_messages": len(channel_messages),
                "active_users": len(set([msg["user"] for msg in channel_messages])),
                "avg_response_time_minutes": random.randint(2, 15),
                "sentiment_analysis": {
                    "overall_sentiment": random.choice(["positive", "neutral", "concerned", "urgent"]),
                    "urgency_level": random.uniform(0.3, 0.9),
                    "collaboration_score": random.uniform(0.7, 0.95)
                },
                "ai_insights": {
                    "communication_effectiveness": random.uniform(0.75, 0.92),
                    "information_clarity": random.uniform(0.70, 0.90),
                    "response_coordination": random.uniform(0.80, 0.95)
                }
            }
        }
    
    def _format_message_by_severity(self, message: str, severity: str) -> str:
        """Format message based on severity level"""
        
        severity_formats = {
            "critical": f"🚨 **CRITICAL ALERT** 🚨\n{message}",
            "high": f"⚠️ **HIGH PRIORITY** ⚠️\n{message}",
            "medium": f"📊 **MEDIUM PRIORITY**\n{message}",
            "low": f"ℹ️ **INFO**\n{message}",
            "info": f"ℹ️ {message}",
            "P0": f"🔴 **P0 INCIDENT** 🔴\n{message}",
            "P1": f"🟠 **P1 INCIDENT** 🟠\n{message}",
            "P2": f"🟡 **P2 INCIDENT** 🟡\n{message}",
            "P3": f"🟢 **P3 INCIDENT** 🟢\n{message}"
        }
        
        return severity_formats.get(severity.lower(), message)
    
    def _calculate_urgency_score(self, severity: str, message: str) -> float:
        """Calculate urgency score for AI prioritization"""
        
        base_scores = {
            "critical": 0.95, "high": 0.8, "medium": 0.6, "low": 0.3, "info": 0.2,
            "P0": 0.95, "P1": 0.8, "P2": 0.6, "P3": 0.4
        }
        
        base_score = base_scores.get(severity.lower(), 0.5)
        
        # Adjust based on message content
        urgent_keywords = ["down", "outage", "critical", "emergency", "urgent", "immediate"]
        keyword_boost = sum(0.1 for keyword in urgent_keywords if keyword.lower() in message.lower())
        
        return min(base_score + keyword_boost, 1.0)
    
    def _analyze_audience_targeting(self, channel: str, message: str) -> Dict[str, Any]:
        """Analyze audience targeting effectiveness"""
        
        channel_audiences = {
            "#incidents": {"primary": "incident_responders", "effectiveness": 0.95},
            "#alerts": {"primary": "monitoring_team", "effectiveness": 0.90},
            "#devops": {"primary": "devops_engineers", "effectiveness": 0.85},
            "#engineering": {"primary": "all_engineers", "effectiveness": 0.70},
            "#on-call": {"primary": "on_call_engineers", "effectiveness": 0.98}
        }
        
        audience_info = channel_audiences.get(channel, {
            "primary": "general_audience",
            "effectiveness": 0.60
        })
        
        return {
            "target_audience": audience_info["primary"],
            "targeting_effectiveness": audience_info["effectiveness"],
            "estimated_relevant_recipients": random.randint(5, 20),
            "noise_level": random.uniform(0.1, 0.4)
        }
    
    def _should_recommend_follow_up(self, severity: str, message: str) -> bool:
        """Determine if follow-up is recommended"""
        
        high_priority = severity.lower() in ["critical", "high", "P0", "P1"]
        contains_action_items = any(word in message.lower() for word in ["investigate", "fix", "resolve", "escalate"])
        
        return high_priority or contains_action_items
    
    def _generate_realistic_reactions(self, severity: str) -> List[Dict[str, Any]]:
        """Generate realistic message reactions"""
        
        reaction_pools = {
            "critical": ["🚨", "👀", "🔥", "⚡", "🆘"],
            "high": ["⚠️", "👍", "🔍", "⏰"],
            "medium": ["👍", "👀", "📊"],
            "low": ["👍", "ℹ️"],
            "info": ["👍", "📝"]
        }
        
        available_reactions = reaction_pools.get(severity.lower(), ["👍"])
        reaction_count = random.randint(0, min(3, len(available_reactions)))
        
        reactions = []
        for _ in range(reaction_count):
            reaction = random.choice(available_reactions)
            reactions.append({
                "name": reaction,
                "count": random.randint(1, 5),
                "users": [random.choice(self.users)["id"] for _ in range(random.randint(1, 3))]
            })
        
        return reactions
    
    def _generate_message_attachments(self, severity: str, message: str) -> List[Dict[str, Any]]:
        """Generate rich message attachments"""
        
        if severity.lower() in ["critical", "high", "P0", "P1"]:
            return [
                {
                    "color": "danger" if severity.lower() in ["critical", "P0"] else "warning",
                    "title": f"{severity.upper()} Incident Alert",
                    "text": "AI-powered incident detection and analysis",
                    "fields": [
                        {"title": "Confidence", "value": f"{random.randint(85, 98)}%", "short": True},
                        {"title": "Response Time", "value": f"{random.randint(30, 180)}s", "short": True},
                        {"title": "Affected Systems", "value": random.choice(["Payment API", "User Service", "Auth Service"]), "short": True},
                        {"title": "Estimated Impact", "value": random.choice(["High", "Medium", "Low"]), "short": True}
                    ],
                    "footer": "AI Incident Response System",
                    "footer_icon": "https://example.com/ai-bot-icon.png",
                    "ts": int(datetime.now().timestamp())
                }
            ]
        
        return []
    
    def _estimate_response_time(self, severity: str, channel: str) -> Dict[str, Any]:
        """Estimate response time based on severity and channel"""
        
        base_times = {
            "critical": {"min": 1, "max": 5, "avg": 2},
            "high": {"min": 2, "max": 10, "avg": 5},
            "medium": {"min": 5, "max": 30, "avg": 15},
            "low": {"min": 15, "max": 60, "avg": 30},
            "P0": {"min": 1, "max": 3, "avg": 2},
            "P1": {"min": 2, "max": 8, "avg": 4},
            "P2": {"min": 5, "max": 20, "avg": 10},
            "P3": {"min": 10, "max": 45, "avg": 20}
        }
        
        time_info = base_times.get(severity.lower(), {"min": 10, "max": 30, "avg": 15})
        
        # Adjust for channel type
        if channel in ["#incidents", "#on-call"]:
            # Faster response in dedicated incident channels
            time_info = {k: max(1, int(v * 0.7)) for k, v in time_info.items()}
        
        return {
            "estimated_response_time_minutes": time_info["avg"],
            "range_minutes": {"min": time_info["min"], "max": time_info["max"]},
            "confidence": random.uniform(0.75, 0.90)
        }
    
    def _get_suggested_incident_members(self, incident_id: str) -> List[str]:
        """Get suggested members for incident channel"""
        
        # Base incident response team
        base_team = ["alice.engineer", "bob.devops", "diana.oncall"]
        
        # Add specialists based on incident type (simulated)
        specialists = ["charlie.sre", "eve.manager", "frank.security", "grace.database"]
        
        # Randomly select additional members
        additional_members = random.sample(specialists, random.randint(1, 3))
        
        return base_team + additional_members
    
    def _generate_communication_strategy(self, incident_id: str) -> Dict[str, Any]:
        """Generate AI communication strategy"""
        
        return {
            "update_frequency": "Every 15 minutes for P0/P1, Every 30 minutes for P2/P3",
            "stakeholder_notifications": [
                "Engineering leadership for P0/P1",
                "Customer success for customer-facing issues",
                "Marketing for public-facing outages"
            ],
            "communication_channels": [
                f"#{incident_id.lower()}-incident",
                "#incidents",
                "Status page updates",
                "Customer notifications"
            ],
            "escalation_triggers": [
                "No progress after 30 minutes",
                "Customer impact increases",
                "Additional services affected"
            ],
            "ai_automation": {
                "auto_updates": True,
                "smart_routing": True,
                "sentiment_monitoring": True,
                "escalation_detection": True
            }
        }
    
    def _generate_escalation_plan(self, incident_id: str) -> Dict[str, Any]:
        """Generate escalation plan"""
        
        return {
            "level_1": {
                "trigger": "Incident detected",
                "actions": ["Notify on-call engineer", "Create incident channel"],
                "timeout_minutes": 15
            },
            "level_2": {
                "trigger": "No resolution after 15 minutes",
                "actions": ["Escalate to senior engineer", "Notify team lead"],
                "timeout_minutes": 30
            },
            "level_3": {
                "trigger": "No resolution after 45 minutes or P0/P1",
                "actions": ["Escalate to engineering manager", "Consider external help"],
                "timeout_minutes": 60
            },
            "level_4": {
                "trigger": "Major outage or extended duration",
                "actions": ["Escalate to VP Engineering", "Activate crisis response"],
                "timeout_minutes": 120
            },
            "ai_monitoring": {
                "auto_escalation": True,
                "escalation_confidence": random.uniform(0.80, 0.95),
                "human_override": True
            }
        }