import React, {Component} from 'react'
import Swal from "sweetalert2"
import Cookies from "universal-cookie"

const local = "http://127.0.0.1:8000/";
const reactLocal = "http://localhost:3000/"
const remote = "https://data-structures-game.herokuapp.com/";

//can also be const url = local; or const url = reactLocal;
const url = local;

/* This class provides the functionality for logging in and out,
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
        if (!this.state.username || !this.state.password1 || this.state.password2 || this.state.email){
            Swal.fire("Please fill in both the username and password fields")
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

            //alert successful login
            Swal.fire({
                title: 'Successfully logged in as ' + this.state.username + '!',
                icon: 'success',
                confirmButtonText: 'Return to Home Page'

                //return to home page if click on button
            }).then((result) => {

                //if player clicks "Return to Home Page" button, redirect there
                if (result.isConfirmed) {
                    window.location.href = "/"
                }
            })
        }

        //if login did not succeed, show error message
        else {
            Swal.fire({
                title: 'User Registration Failed',
                icon: 'error',

                //may add "Forgot password" option later
                text: 'If you believe this is a mistake, please try authenticating again'
            })
        }
    }

    //make api call to log out
    handleInput = async (e) => {
        await this.setState({ [e.target.name]: e.target.value })
    }

    //update stored username when user types
    handleUserChange = (event) => {
        this.setState({
            username: event.target.value
        })
    }

    //update stored password when user types
    handlePassChange = (event) => {
        this.setState({
            password: event.target.value
        })
    }

    render() {
        return (
            <form class="container mx-auto h-full flex justify-center items-center align-center">
                <div class="w-1/2 font-thin">

                    {/*Header*/}
                    <h1 class="mt-12 mb-6 text-3xl text-center">
                        Create a new profile
                    </h1>

                    {/*Username and password boxes*/}
                    <div class="align-center items-center">
                    <div class="py-4 px-3">
                        <label class="text-xl ml-32 px-4">
                            Username:
                        </label>
                        <input class="bg-gray-200 shadow border-blue-500 border rounded w-48 py-2 px-2 text-gray-700"
                               name="username" id="username1" type="text" value={this.state.username}
                               onChange={this.handleInput}>
                        </input>
                        </div>
                        <div class="py-4 px-3">
                        <label className="text-xl ml-32 px-3">
                            Email:
                        </label>
                        <input className="bg-gray-200 shadow border-blue-500 border rounded w-48 py-2 px-2 text-gray-700"
                               name="email" id="email" type="text" value = {this.state.email}
                               onChange={this.handleInput}>
                        </input>
                        </div>


                        <div class="py-4 px-3">
                        <label className="text-xl ml-32 px-3">
                            Password:
                        </label>
                        <input className="bg-gray-200 shadow border-blue-500 border rounded w-48 py-2 px-2 text-gray-700"
                               name="password1" id="password1" type="password" placeholder="******************" value = {this.state.password1}
                               onChange={this.handleInput}>
                        </input>
                        </div>

                        <div class="py-4 px-3">
                        <label className="text-xl ml-32 px-3">
                            Re-Enter Password:
                        </label>
                        <input className="bg-gray-200 shadow border-blue-500 border rounded w-48 py-2 px-2 text-gray-700"
                               name="password2" id="password2" type="password" placeholder="******************" value = {this.state.password2}
                               onChange={this.handleInput}>
                        </input>
                        </div>
                    </div>

                    <div>
                        {/*When user clicks "Sign in", make api call*/}
                        <button class="bg-blue-500 text-white hover:bg-blue-700 ml-64 w-32 font-bold rounded py-2 px-4"
                            id="login-btn" type="button"
                            onClick={() => this.registerFxn()}>
                            Register
                        </button>
                    </div>
                </div>
            </form>
        )
    }
}

export default Register;