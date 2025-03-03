import { useEffect, useState } from "react";
import axios from "axios";

const Dashboard = () => {
  const [doctors, setDoctors] = useState([]);

  useEffect(() => {
    const fetchDoctors = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/doctors/");
        setDoctors(response.data);
      } catch (error) {
        console.error("Error fetching doctors:", error);
      }
    };

    fetchDoctors();
  }, []);

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Available Doctors</h2>
      <div className="row">
        {doctors.length > 0 ? (
          doctors.map((doctor) => (
            <div key={doctor.id} className="col-md-4">
              <div className="card shadow-sm mb-4">
                <div className="card-body">
                  <h5 className="card-title">{doctor.firstname} {doctor.lastname}</h5>
                  <p className="card-text"><strong>Email:</strong> {doctor.email}</p>
                  <p className="card-text"><strong>Contact:</strong> {doctor.contact || "N/A"}</p>
                  <button className="btn btn-primary w-100">Book Appointment</button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <p className="text-center">No doctors available.</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
