import { useAuth } from "../contexts/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  const handleSignOut = async () => {
    await signOut();
    navigate("/login");
  };

  return (
    <div>
      <header>
        <h1>Costhook</h1>
        <div>
          <span>{user?.email}</span>
          <button onClick={handleSignOut}>Sign Out</button>
        </div>
      </header>
      <main>
        <h2>Dashboard</h2>
        <p>Welcome to Costhook! Start monitoring your costs across providers.</p>
      </main>
    </div>
  );
}
