from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from ..utils.config import get_database_config

Base = declarative_base()
engine = create_engine(get_database_config()["url"])
Session = sessionmaker(bind=engine)

class Application(Base):
    """Model for tracking job applications."""
    
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String(255), nullable=False)
    position_title = Column(String(255), nullable=False)
    job_description = Column(Text)
    submission_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="submitted")
    resume_version = Column(String(255))
    cover_letter_version = Column(String(255))
    
    # Relationships
    emails = relationship("Email", back_populates="application")
    
    @classmethod
    def get_by_id(cls, application_id: int):
        """Get application by ID."""
        session = Session()
        return session.query(cls).filter(cls.id == application_id).first()

class Email(Base):
    """Model for tracking email communications."""
    
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    subject = Column(String(255))
    content = Column(Text)
    sent_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="pending")
    
    # Relationships
    application = relationship("Application", back_populates="emails")

class EmailTemplate(Base):
    """Model for storing email templates."""
    
    __tablename__ = "email_templates"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    subject = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    
    @classmethod
    def get_by_name(cls, name: str):
        """Get template by name."""
        session = Session()
        return session.query(cls).filter(cls.name == name).first()

def init_db():
    """Initialize the database."""
    Base.metadata.create_all(engine)
    
    # Create default email templates
    session = Session()
    
    # Application template
    if not session.query(EmailTemplate).filter(EmailTemplate.name == "application").first():
        application_template = EmailTemplate(
            name="application",
            subject="Application for {{ position_title }} position",
            content="""
            Dear {{ hiring_manager }},
            
            I am writing to express my strong interest in the {{ position_title }} position at {{ company_name }}.
            
            {{ custom_content }}
            
            Thank you for considering my application.
            
            Best regards,
            {{ applicant_name }}
            """
        )
        session.add(application_template)
    
    # Follow-up template
    if not session.query(EmailTemplate).filter(EmailTemplate.name == "follow_up").first():
        follow_up_template = EmailTemplate(
            name="follow_up",
            subject="Following up on {{ position_title }} application",
            content="""
            Dear {{ hiring_manager }},
            
            I hope this email finds you well. I am writing to follow up on my application for the {{ position_title }} position at {{ company_name }}, which I submitted on {{ submission_date }}.
            
            I remain very interested in the opportunity and would welcome the chance to discuss how I can contribute to your team.
            
            Thank you for your time and consideration.
            
            Best regards,
            {{ applicant_name }}
            """
        )
        session.add(follow_up_template)
    
    session.commit()
