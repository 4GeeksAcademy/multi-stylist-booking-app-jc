import enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Enum, DateTime, func, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class UserRole(enum.Enum):
    stylist = "stylist"
    client = "client"


class AppointmentStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    canceled = "canceled"
    completed = "completed"


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
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    stylist: Mapped[list['Stylist']] = relationship(back_populates='user')
    client: Mapped[list['Client']] = relationship(back_populates='userClient')

    def serialize(self):
        return {
            "id": self.id,

            "email": self.email,
        }


class Stylist(db.Model):
    __tablename__ = 'stylist'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    bio: Mapped[str] = mapped_column(String(500))
    phone: Mapped[int] = mapped_column(Integer, nullable=False)
    address: Mapped[float] = mapped_column(String(120), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    profile_image: Mapped[str] = mapped_column(String, nullable=False)
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    user: Mapped['User'] = relationship(back_populates='stylist')
    services: Mapped[list['Services']] = relationship(
        back_populates='stylistServices')
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
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    address: Mapped[str] = mapped_column(String(120), nullable=True)
    phone: Mapped[int] = mapped_column(Integer, nullable=True)
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
    stylist_id: Mapped[int] = mapped_column(ForeignKey('stylist.id'))
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
    __tablename__ = 'services'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stylist_id: Mapped[int] = mapped_column(ForeignKey('services.id'))
    day_of_week: Mapped[str] = mapped_column(String(), nullable=False)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    stylistAvailability: Mapped['Stylist'] = relationship(
        back_populates='availability')


class Appointments(db.Model):
    __tablename__ = 'appointments'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stylist_id: Mapped[int] = mapped_column(ForeignKey('stylist.id'))
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'))
    services_id: Mapped[int] = mapped_column(ForeignKey('services.id'))
    apointment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())
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


class Messages(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stylist_id: Mapped[int] = mapped_column(ForeignKey('stylist.id'))
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'))
    appointment_id: Mapped[int] = mapped_column(ForeignKey('appointments.id'))
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
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stylist_id: Mapped[int] = mapped_column(ForeignKey('stylist.id'))
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'))
    appointment_id: Mapped[int] = mapped_column(ForeignKey('appointments.id'))
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(String(500))
    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    stylistReview: Mapped['Stylist'] = relationship(back_populates='review_by')
    clientReview: Mapped['Client'] = relationship(
        back_populates='reviewClient')
    appointmentReview: Mapped['Appointments'] = relationship(
        back_populates='reviewaApointment')
