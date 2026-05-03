import "../Dashboard/Dashboard.css";

const SearchEmployees = ({ onSearch }) => {
  return (
    <div>
      <input
        type="text"
        placeholder="Search employees..."
        className="search-input"
        onChange={(e) => onSearch?.(e.target.value)}
      />
    </div>
  );
};

export default SearchEmployees;
