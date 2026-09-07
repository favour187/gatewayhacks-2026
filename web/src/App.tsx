import { AuthProvider } from "./lib/auth";
import { APP } from "./appConfig";

export default function App() {
  return (
    <AuthProvider>
      <header className="app-header">
        <div className="app-brand">
          <span className="app-logo">◈</span>
          <span>{APP.name}</span>
        </div>
      </header>
      <main className="app-main">
        <p>{APP.name}</p>
      </main>
    </AuthProvider>
  );
}
