import { useState } from "react"
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";
import { Navigate, useNavigate } from "react-router-dom";


export const LoginProvider = () => {

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const { store, dispatch } = useGlobalReducer();

    const navigate = useNavigate()

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const resp = await fetch(`${import.meta.env.VITE_BACKEND_URL}api/user/provider/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            })
            const data = await resp.json()
            console.log(data)

            if (resp.ok)
                localStorage.setItem('provider', JSON.stringify(data.provider))
                localStorage.setItem('token', data.token)

            dispatch({
                type: 'login-provider',
                payload: {
                    provider: data.provider,
                    token: data.token
                }
            })

            navigate('/providerDashboard')

        } catch (error) {
            console.error('Error de connexion en el servidedor', error)
        }

    }

    return (
        <div>
            <form onSubmit={handleLogin}
                className="row g-3">
                <div className="col-12">
                    <label className="form-label">Email</label>
                    <input type="email" className="form-control" id="inputEmail4"
                        onChange={(e) => setEmail(e.target.value)} value={email}
                    />
                </div>
                <div className="col-12">
                    <label className="form-label">Password</label>
                    <input type="password" className="form-control" id="inputPassword4"
                        onChange={(e) => setPassword(e.target.value)} value={password}
                    />
                </div>
                <div className="col-12">
                    <button type="submit" className="btn btn-primary">Sign in</button>
                </div>
            </form>
        </div>
    )
}
