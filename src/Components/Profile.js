import React, {Component} from 'react'
import Swal from "sweetalert2"
import Cookies from "universal-cookie"
import Particles from "react-particles-js"

//Fix XSS security issues when developing locally
//this allows us to test separately locally and on Heroku by changing just one line
const local = "http://127.0.0.1:8000/";
const reactLocal = "http://localhost:3000/"
const remote = "https://data-structures-game.herokuapp.com/";

//can also be const url = local; or const url = reactLocal;
const url = local;

/* This class provides the functionality for logging in and out,
   registering a new account and (eventually) adding friends
   and viewing user's profile info
 */
class Profile extends Component {
    constructor(props) {
        super(props);

        //see if logged in when profile page called
        const cookies = new Cookies();
        let prevLogin //for checking if logged in already, true if already logged in
        if ((cookies.get('token')) && (cookies.get('token') != '')){
            prevLogin = true
        }
        else {
            prevLogin = false
        }

        //store the username and password that a user types in
        this.state = {
            username: null,
            password: null,
            loggedIn: prevLogin
        }
    }

    //api call to login
    //Note: api uses FormData for this call
    loginFxn = async () => {

        //if either field is blank, prompt user for input
        if (!this.state.username || !this.state.password){
            Swal.fire("Please fill in both the username and password fields")
            return
        }

        //hash password
        let CryptoJS = require("crypto-js")

        //use username as salt for SHA-256 hash, so combine username and plaintext pw into one string
        let toHash = this.state.username + this.state.password

        //hash it and convert to string format
        let hashed = CryptoJS.SHA256(toHash)
        hashed = hashed.toString()

        //store user input in FormData format
        let user_and_pass = new FormData()
        user_and_pass.append("user_id", this.state.username)
        user_and_pass.append("password", hashed)

        //api call parameters
        let requestOptions = {
            method: 'POST',
            body: user_and_pass,
            redirect: 'follow'
        };

        //make api call
        let fetch_url = url + "profile_page/api/login"
        let response = await fetch(fetch_url, requestOptions);
        let returned = await response.json();

        //if login attempt was successful
        if (returned["status"] == "success") {

            //store authentication token in a cookie
            const cookies = new Cookies()
            cookies.set('token', returned["token"], { path: '/' })
            cookies.set('username', this.state.username, { path: '/'})

            //update state to reflect successful login
            this.setState({loggedIn: true})

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
                title: 'Login Failed',
                icon: 'error',

                //may add "Forgot password" option later
                text: 'If you believe this is a mistake, please try authenticating again'
            })
        }
    }

    //make api call to log out
    logoutFxn = async () => {
        const cookies = new Cookies()

        console.log("In logout, printing token: ", cookies.get('token'))

        //format user_id and token as FormData
        let user_and_token = new FormData()
        user_and_token.append("user_id", cookies.get('username'))
        user_and_token.append("token", cookies.get('token'))

        //request options
        let requestOptions = {
            method: 'POST',
            body: user_and_token,
            redirect: 'follow'
        };

        //make api call
        let fetch_url = url + "profile_page/api/logout"
        let response = await fetch(fetch_url, requestOptions);
        let returned = await response.json();

        //successful logout
        if (returned["status"] == "success"){

            //remove cookies and set to empty to double-check
            cookies.remove('username', { path: '/'})
            cookies.remove('token', { path: '/'})
            cookies.set('username', '', { path: '/'})
            cookies.set('token', '', { path: '/'})

            this.setState({loggedIn: false})

            //show popup
            Swal.fire({
                title: 'Logout Successful!',
                icon: 'success',
                text: 'Come back soon!'
            })
        }

        //error when attempt to logout - popup
        else {
            Swal.fire({
                title: 'Logout Unsuccessful',
                icon: 'error',
                text: "Please make sure you're signed in"
            })
        }
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

    //function for displaying the login screen
    displayLogIn = () => {
        return (
            <div>
                <Particles
                        id="particles"
                        params={{
                        particles: {
                            color:"#000000",
                            line_linked: {
                            color:"#000000",
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
                    <div className="w-full md:max-w-md mt-6 md:justify-items-center flex mx-auto my-auto">

                  <span>

                    <div className="bg-blue-200 shadow-2xl rounded-2xl px-4 py-4 space-y-20 space-x-20">
                        <form>
                            <div class="font-thin space-y-12 space-x-12">

                            {/*Header*/}
                            <h1 class="text-3xl text-center py-2">
                                Login to view your profile!
                            </h1>

                            {/*Username and password boxes*/}
                            <div class="space-x-2 space-y-2 md:justify-items-center">
                                <label class="text-xl px-3 justify-center">
                                    Username:
                                </label>
                            <input
                                class="bg-gray-200 shadow border-blue-500 border rounded py-2 px-2 text-gray-700"
                                id="username" type="text" value={this.state.username}
                                onChange={this.handleUserChange}>
                            </input>

                            <div class="space-x-1 space-y-2">
                                <label className="text-xl py-4 px-3 justify-center">
                                    Password:
                                </label>
                                <input
                                    className="bg-gray-200 shadow border-blue-500 border rounded py-2 px-2 text-gray-700"
                                    id="password" type="password" placeholder="******************"
                                    value={this.state.password}
                                    onChange={this.handlePassChange}>
                                </input>
                            </div>

                            <div class="py-8 px-16">
                                {/*When user clicks "Sign in", make api call*/}
                                <button
                                    class="bg-blue-500 text-white hover:bg-blue-700 w-32 font-bold rounded py-2 px-4"
                                    id="login-btn" type="button"
                                    onClick={() => this.loginFxn()}>
                                    Sign in
                                </button>
                            </div>
                            </div>
                        </div>
                        </form>
                    </div></span></div></div>
        )
    }

    //display user profile and sign out button
    displayUserProfile = () => {
        return(<div>
            <Particles
                id="particles"
                params={{
                particles: {
                    color:"#000000",
                    line_linked: {
                    color:"#000000",
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
            {/*When user clicks "Sign out", make api call to log out*/}
            <button
                className="bg-red-500 text-white hover:bg-red-700 font-bold w-32 rounded px-4 py-2 mt-6 ml-64"
                id="logout-btn" type="button"
                onClick={() => this.logoutFxn()}>
                Sign out?
            </button>
        </div>)
    }

    render() {
        //display login screen if not logged in
        const cookies = new Cookies()
        if ((this.state.loggedIn === false) || (cookies.get('token') === '')){
            return (this.displayLogIn())
        }

        //display user profile page with option to log out
        else {
            return(this.displayUserProfile())
        }
    }
}
export default Profile