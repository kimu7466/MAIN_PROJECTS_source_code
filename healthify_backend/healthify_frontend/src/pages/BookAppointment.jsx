import { useState } from "react";
import axios from "axios";

const BookAppointment = () => {
  const [formData, setFormData] = useState({ patient: "", doctor: "", date: "", time: "" });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://127.0.0.1:8000/book-appointment/", formData);
      alert("Appointment booked successfully!");
    } catch (error) {
      alert("Error booking appointment!");
    }
  };

  return (
    <div className="container mt-5">
      <div className="card shadow-sm p-4">
        <h2 className="text-center mb-4">Book an Appointment</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Patient ID</label>
            <input type="text" name="patient" className="form-control" placeholder="Enter Patient ID" onChange={handleChange} required />
          </div>

          <div className="mb-3">
            <label className="form-label">Doctor ID</label>
            <input type="text" name="doctor" className="form-control" placeholder="Enter Doctor ID" onChange={handleChange} required />
          </div>

          <div className="mb-3">
            <label className="form-label">Appointment Date</label>
            <input type="date" name="date" className="form-control" onChange={handleChange} required />
          </div>

          <div className="mb-3">
            <label className="form-label">Appointment Time</label>
            <input type="time" name="time" className="form-control" onChange={handleChange} required />
          </div>

          <button type="submit" className="btn btn-primary w-100">Book Appointment</button>
        </form>
      </div>
    </div>
  );
};

export default BookAppointment;
