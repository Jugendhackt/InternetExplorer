import { useEffect, useState } from "react";
import { Moon, Sun } from "react-bootstrap-icons";

const STORAGE_KEY = "darkModeEnabled";

const ColorSchemeToggle = () => {
  const [isDarkModeEnabled, setDarkModeEnabled] = useState(false);

  useEffect(() => {
    const value = localStorage.getItem(STORAGE_KEY);
    if (value == null) {
      return;
    }
    const darkModeEnabled = JSON.parse(value);
    if (darkModeEnabled) {
      setDarkModeEnabled(darkModeEnabled);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(isDarkModeEnabled));
    document.documentElement.setAttribute(
      "data-bs-theme",
      isDarkModeEnabled ? "dark" : "light"
    );
  }, [isDarkModeEnabled]);

  function toggleDarkMode() {
    setDarkModeEnabled(!isDarkModeEnabled);
  }

  if (isDarkModeEnabled) {
    return <Moon onClick={toggleDarkMode} />;
  }

  return <Sun onClick={toggleDarkMode} />;
};

export default ColorSchemeToggle;
