function StatCard({ title, value, icon }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>

      <div>
        <p className="stat-title">{title}</p>
        <h2>{value}</h2>
      </div>
    </div>
  );
}

export default StatCard;