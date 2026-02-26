import { Navigate } from "react-router-dom"

export const PrivateProviderRoute = ({ children }) => {

    const token = localStorage.getItem("provider")

    if (!token) {
        return <Navigate to="/loginprovider" />
    }
    return children
}