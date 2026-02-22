import enum
from datetime import datetime, time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Enum, DateTime, func, ForeignKey, Float, UniqueConstraint, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class UserRole(enum.Enum):
    STYLIST = "stylist"
    CLIENT = "client"


class AppointmentStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    canceled = "canceled"
    completed = "completed"


class PaymentMethod(enum.Enum):
    card = "card"
    pix = "pix"
    cash = "cash"


class PaymentStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    refunded = "refunded"
    failed = "failed"


class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)

    stylist: Mapped['Stylist'] = relationship(back_populates='user')
    client: Mapped['Client'] = relationship(back_populates='userClient')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class Provider(db.Model):
    __tablename__ = 'provider'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(500) nullable=False)
    address: Mapped[str] = mapped_column(String(120), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    logo_image: Mapped[str] = mapped_column(String(), nullable=False)
    cover_image: Mapped[str] = mapped_column(String(20), nullable=False)
    is_verified: Mapped[bool] = mapped_column[Boolean]
    create_at: Mapped[datetime] = mapped_column[datetime]


class Stylist(db.Model):
    __tablename__ = 'stylist'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider_id: Mapped[int] = mapped_column(
        ForeignKey('provider.id'), nullable=True)
    name: Mapped[str] = mapped_column(String(120))
    instagram_url: Mapped[str] = mapped_column(String(20), nullable=False)
    profile_image: Mapped[str] = mapped_column(String, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean)
    is_active: Mapped[bool] = mapped_column(Boolean)

    user: Mapped['User'] = relationship(back_populates='stylist')
    services: Mapped[list['Services']] = relationship(
        back_populates='stylistServices', cascade='all, delete-orphan')
    availability: Mapped[list['Availability']] = relationship(
        back_populates='stylistAvailability')
    appointment: Mapped[list['Appointments']] = relationship(
        back_populates='stylistAppointment')
    messageStylist: Mapped[list['Messages']] = relationship(
        back_populates='stylistMessage')
    review_by: Mapped[list['Review']] = relationship(
        back_populates='stylistReview')


class Client(db.Model):
    __tablename__ = 'client'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    address: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    userClient: Mapped['User'] = relationship(back_populates='client')
    appointment_by: Mapped[list['Appointments']] = relationship(
        back_populates='clientAppointment')
    clientMessage: Mapped[list['Messages']] = relationship(
        back_populates='clientMessage')
    reviewClient: Mapped[list['Review']] = relationship(
        back_populates='clientReview')


class Services(db.Model):
    __tablename__ = 'services'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stylist_id: Mapped[int] = mapped_column(
        ForeignKey('stylist.id'), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    price: Mapped[float] = mapped_column(Float)
    duration: Mapped[int] = mapped_column(Integer)
    image: Mapped[str] = mapped_column(String())
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    stylistServices: Mapped['Stylist'] = relationship(
        back_populates='services')
    appointmentServices: Mapped[list['Appointments']] = relationship(
        back_populates='servicesAppointment')


class Availability(db.Model):
    __tablename__ = 'availability'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stylist_id: Mapped[int] = mapped_column(
        ForeignKey('stylist.id'), nullable=False)
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    start_time: Mapped[time] = mapped_column(
        db.Time(timezone=True), nullable=True)
    end_time: Mapped[time] = mapped_column(
        db.Time(timezone=True), nullable=False)

    stylistAvailability: Mapped['Stylist'] = relationship(
        back_populates='availability')


class Appointments(db.Model):
    __tablename__ = 'appointments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stylist_id: Mapped[int] = mapped_column(
        ForeignKey('stylist.id'), nullable=False)
    client_id: Mapped[int] = mapped_column(
        ForeignKey('client.id'), nullable=False)
    services_id: Mapped[int] = mapped_column(
        ForeignKey('services.id'), nullable=False)
    apointment_date: Mapped[datetime] = mapped_column(
        Date, nullable=False)
    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(AppointmentStatus), nullable=False)
    price: Mapped[float] = mapped_column(Float)
    note: Mapped[str] = mapped_column(String(500))
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    stylistAppointment: Mapped['Stylist'] = relationship(
        back_populates='appointment')
    clientAppointment: Mapped['Client'] = relationship(
        back_populates='appointment_by')
    servicesAppointment: Mapped['Services'] = relationship(
        back_populates='appointmentServices')
    messageAppointment: Mapped[list['Messages']] = relationship(
        back_populates='appoinmentMessage')
    reviewaApointment: Mapped[list['Review']] = relationship(
        back_populates='appointmentReview')


class Payment(db.Model):
    __tablename__ = 'payment'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    appointments_id: Mapped[int] = mapped_column(
        ForeignKey('appointments.id'), nullable=False)
    provider_id: Mapped[int] = mapped_column(
        ForeignKey('provider.id'), nullable=False)
    amount: Mapped[float] = mapped_column(float, nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod), nullable=False)
    curency: Mapped[str] = mapped_column(String(), nullable=False)
    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus), nullable=False)
    transaction_id: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())


class Messages(db.Model):
    __tablename__ = 'messages'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stylist_id: Mapped[int] = mapped_column(
        ForeignKey('stylist.id'), nullable=False)
    client_id: Mapped[int] = mapped_column(
        ForeignKey('client.id'), nullable=False)
    appointment_id: Mapped[int] = mapped_column(
        ForeignKey('appointments.id'), nullable=False)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean)
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    stylistMessage: Mapped['Stylist'] = relationship(
        back_populates='messageStylist')
    clientMessage: Mapped['Client'] = relationship(
        back_populates='clientMessage')
    appoinmentMessage: Mapped['Appointments'] = relationship(
        back_populates='messageAppointment')


class Review(db.Model):
    __tablename__ = 'review'
    __table_args__ = (UniqueConstraint('appointment_id',
                      name='only_review_per_appointment'),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stylist_id: Mapped[int] = mapped_column(
        ForeignKey('stylist.id'), nullable=False)
    client_id: Mapped[int] = mapped_column(
        ForeignKey('client.id'), nullable=False)
    appointment_id: Mapped[int] = mapped_column(
        ForeignKey('appointments.id'), nullable=False)
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(String(500))
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    stylistReview: Mapped['Stylist'] = relationship(back_populates='review_by')
    clientReview: Mapped['Client'] = relationship(
        back_populates='reviewClient')
    appointmentReview: Mapped['Appointments'] = relationship(
        back_populates='reviewaApointment')


class PortfolioProject(db.Model):
    __tablename__ = 'portfolioproject'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stylist_id: Mapped[int] = mapped_column(
        ForeignKey('stylist.id'), nullable=False)
    title: Mapped[str] = mapped_column(String())
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())


class PortfolioImage(db.Model):
    __tablename__ = 'portfolioimage'
    id: Mapped[int] = mapped_column(Integer, primarru_key=True)
    portfolioproject_id: Mapped[int] = mapped_column(
        ForeignKey('portfolioproject.id'), nullable=False)
    image_url:  Mapped[str] = mapped_column(String(500), nullable=False)
    is_corver: Mapped[bool] = mapped_column[Boolean]
    order_index: Mapped[int] = mapped_column(Integer)


class Specialties(db.Model):
    __tablename__ = 'specialities'
    id: Mapped[int] = mapped_column(Integer, primarru_key=True)
    name: Mapped[str] = mapped_column(String(120))
    slug: Mapped[str] = mapped_column(String(120))
    category: Mapped[str] = mapped_column(String(120))


class StylistSpecialty(db.Model):
    id: Mapped[int] = mapped_column(Integer, primarru_key=True)
    stylist_id: Mapped[int] = mapped_column(
        ForeignKey('stylist.id'), nullable=False)
    specialties_id: Mapped[int] = mapped_column(
        ForeignKey('specialities.id'), nullable=False)
