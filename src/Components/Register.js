import React, {Component} from 'react'
import Swal from "sweetalert2"
import Cookies from "universal-cookie"
import Particles from "react-particles-js"



const local = "http://127.0.0.1:8000/";
const reactLocal = "http://localhost:3000/"
const remote = "https://data-structures-game.herokuapp.com/";

//can also be const url = local; or const url = reactLocal;
const url = local;

/* This class provides the functionality for registering only,
   registering a new account and (eventually) adding friends
   and viewing user's profile info
 */
class Register extends Component {
    constructor(props) {
        super(props);

        //store the username and password that a user types in
        this.state = {
            username: null,
            password1: null,
            password2: null,
            email:null

        }
    }

    //api call to login
    //Note: api uses FormData for this call
    registerFxn = async () => {

        //if either field is blank, prompt user for input
        if (!this.state.username || !this.state.password1 || !this.state.password2 || !this.state.email){
            Swal.fire("Please fill all fields")
            return
        }

        //hash password
        let CryptoJS = require("crypto-js")

        //use username as salt for SHA-256 hash, so combine username and plaintext pw into one string
        let toHash1 = this.state.username + this.state.password1
        let toHash2 = this.state.username + this.state.password2
        //hash it and convert to string format
        let hashed1 = CryptoJS.SHA256(toHash1)
        hashed1 = hashed1.toString()
        let hashed2 = CryptoJS.SHA256(toHash2)
        hashed2 = hashed2.toString()
        //store user input in FormData format
        let registerInfo = new FormData()
        registerInfo.append("user_name", this.state.username)
        registerInfo.append("password1", hashed1)
        registerInfo.append("password2", hashed2)
        registerInfo.append("email", this.state.email)

        //api call parameters
        let requestOptions = {
            method: 'POST',
            body: registerInfo,
            redirect: 'follow'
        };

        //make api call
        let fetch_url = url + "profile_page/api/register"
        let response = await fetch(fetch_url, requestOptions);
        let returned = await response.json();
      
        //if login attempt was successful
        if (returned["status"] == "success") {

            //store authentication token in a cookie
            const cookies = new Cookies()
            cookies.set('token', returned["token"], { path: '/' })
            cookies.set('username', this.state.username, { path: '/'})

            //alert successful registration
            Swal.fire({
                title: 'Successfully registered!',
                icon: 'success',
                confirmButtonText: 'User Profile'

                //return to profile page if click on button
            }).then((result) => {

                //if player clicks "User Profile" button, redirect there
                if (result.isConfirmed) {
                    window.location.href = "/profile_page"
                }
            })
        }

        //if registration did not succeed, show error message
        else {

            Swal.fire({
                title: 'User Registration Failed',
                icon: 'error',
                text: returned['error']
            })
        }

    }

    //make api call to log out
    handleInput = async (e) => {
        await this.setState({ [e.target.name]: e.target.value })
       
    }


    render() {
        return (
            <div>
            <Particles
                id="particles"
                params={{
                    particles: {
                        color: "#000000",
                        line_linked: {
                            color: "#000000",
                        },
                        number: {
                            value: 80,
                            density: {
                                enable: true,
                                value_area: 800,
                            }
                        },
                    },
                }}
            />
            <div className="flex items-center justify-center h-screen">
                <div className="w-full md:max-w-md mt-6">
                    <span>
                        <div className="card bg-gray-200 shadow-2xl rounded-2xl px-4 py-4 mb-4 ">

                            <div className="space-y-10 flex justify-center">
                                <h1 className="space-y-20 text-3xl text-center font-semibold text-gray-800 mb-2">Register to create your profile!</h1>
                            </div>

                            <form>

                                <div className="space-y-2 p-3 items-center">
                                    <label className="text-xl text-left font-semibold text-gray-800 mb-2 px-3">
                                        Username:
                                    </label>
                                    <input
                                        className="bg-gray-200 shadow border-blue-500 border rounded py-2 pl-40  text-gray-700"
                                        name="username" id="username" type="text" value={this.state.username}
                                        onChange={this.handleInput}>
                                    </input>
                                </div>


                                <div className="space-y-2 p-3 items-center">
                                    <label className="text-xl text-left font-semibold text-gray-800 mb-2 px-3">
                                        Email:
                                    </label>
                                    <input
                                        className="bg-gray-200 shadow border-blue-500 border rounded py-2 pl-40  text-gray-700"
                                        name="email" id="email" type="text" value={this.state.email}
                                        onChange={this.handleInput}>
                                    </input>
                                </div>

                                <div className="space-y-2 px-3 items-center">
                                    <label className="text-xl text-left font-semibold text-gray-800 mb-2 px-4">
                                        Password:
                                    </label>
                                    <input
                                        className="bg-gray-200 shadow border-blue-500 border rounded py-2 pl-40 text-gray-700"
                                        name="password1" id="password1" type="password" placeholder="******************"
                                        value={this.state.password1}
                                        onChange={this.handleInput}>
                                    </input>
                                </div>



                                <div className="space-y-2 px-3 items-center">
                                    <label className="text-xl text-left font-semibold text-gray-800 mb-2 px-4">
                                        Verify Password:
                                    </label>
                                    <input
                                        className="bg-gray-200 shadow border-blue-500 border rounded py-2 pl-40  text-gray-700"
                                        name="password2" id="password2" type="password" placeholder="******************"
                                        value={this.state.password2}
                                        onChange={this.handleInput}>
                                    </input>
                                </div>





                                <div className="space-y-10"><br></br></div>
                                {/*When user clicks "Register", make api call*/}
                                <button
                                    className="shadow transition duration-500 ease-in-out bg-blue-500 hover:bg-red-500 transform hover:-translate-y-1 hover:scale-105 bg-blue-300 border-blue-350 border-opacity-50 rounded-lg shadow-xl mx-32 px-10 py-3 rounded spacing-y-3 spacing-x-10 text-xl font-bold"
                                    id="login-btn" type="button"
                                    onClick={() => this.registerFxn()}>
                                    Register
                                </button>
                                <div className="space-y-10"><br></br></div>

                            </form>

                        </div></span></div></div></div>






        )
    }
}

export default Register;