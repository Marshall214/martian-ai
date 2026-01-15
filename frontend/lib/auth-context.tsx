"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"
import { useRouter } from "next/navigation"
import { signupUser, loginUser, getLoggedInUser } from "./services/auth"

interface User {
  id: number
  email: string
  full_name?: string
}

interface AuthContextType {
  user: User | null
  token: string | null
  login: (email: string, password: string) => Promise<void>
  signup: (fullName: string | undefined, email: string, password: string) => Promise<void>
  logout: () => void
  isLoading: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isClient, setIsClient] = useState(false) // New state for client-side check
  const router = useRouter()

  useEffect(() => {
    setIsClient(true) // Set to true once on the client
  }, [])

  useEffect(() => {
    if (isClient) { // Only run on client side
      const storedToken = localStorage.getItem("jwt_token")
      if (storedToken) {
        setToken(storedToken)
        fetchUser(storedToken)
      }
      setIsLoading(false)
    }
  }, [isClient]) // Depend on isClient

  const fetchUser = async (jwtToken: string) => {
    try {
      const userDetails = await getLoggedInUser(jwtToken)
      setUser(userDetails)
    } catch (error) {
      console.error("Failed to fetch user details:", error)
      logout()
    }
  }

  const login = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      const { access_token } = await loginUser(email, password)
      localStorage.setItem("jwt_token", access_token)
      setToken(access_token)
      await fetchUser(access_token)
      router.push("/dashboard")
    } catch (error) {
      console.error("Login failed:", error)
      throw error // Re-throw to allow component to handle error display
    } finally {
      setIsLoading(false)
    }
  }

  const signup = async (fullName: string | undefined, email: string, password: string) => {
    setIsLoading(true)
    try {
      const { access_token } = await signupUser(fullName, email, password)
      localStorage.setItem("jwt_token", access_token)
      setToken(access_token)
      await fetchUser(access_token)
      router.push("/dashboard")
    } catch (error) {
      console.error("Signup failed:", error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem("jwt_token")
    router.push("/login")
  }

  if (isLoading && !isClient) {
    return <div>Loading authentication...</div>; // Or a more sophisticated loading spinner
  }

  return <AuthContext.Provider value={{ user, token, login, signup, logout, isLoading }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
