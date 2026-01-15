const BASE_URL = "http://localhost:8000";

interface AuthResponse {
  access_token: string;
  token_type: string;
}

interface UserDetails {
  id: number;
  email: string;
  full_name?: string;
}

export const signupUser = async (fullName: string | undefined, email: string, password: string): Promise<AuthResponse> => {
  const response = await fetch(`${BASE_URL}/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ full_name: fullName, email, password }),
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Signup failed");
  }
  return response.json();
};

export const loginUser = async (email: string, password: string): Promise<AuthResponse> => {
  const form_data = new URLSearchParams();
  form_data.append("username", email);
  form_data.append("password", password);

  const response = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: form_data.toString(),
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Login failed");
  }
  return response.json();
};

export const getLoggedInUser = async (token: string): Promise<UserDetails> => {
  const response = await fetch(`${BASE_URL}/auth/me`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to fetch user details");
  }
  return response.json();
};
