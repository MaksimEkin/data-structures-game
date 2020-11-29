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
            loggedIn: prevLogin,
            userPoints: null,
            userRank: null
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
                <div className="flex items-center justify-center h-screen">
                <div className="w-full md:max-w-md mt-6">
            <span>
            <div className="card bg-gray-200 shadow-2xl rounded-2xl px-4 py-4 mb-4 ">

            <div className="space-y-10 flex justify-center">
              <h1 className="space-y-20 text-3xl text-center font-semibold text-gray-800 mb-2">Login to view your profile!</h1>
          </div>

        <form>

        <div className="space-y-2 p-3 items-center">
        <label className="text-xl text-center font-semibold text-gray-800 mb-2 px-3">
            Username:
        </label>
                <input
                    className="bg-gray-200 shadow border-blue-500 border rounded py-2 px-2 text-gray-700"
                    id="username" type="text" value={this.state.username}
                    onChange={this.handleUserChange}>
                </input>
        </div>

        <div className="space-y-2 px-3 items-center">
        <label className="text-xl text-center font-semibold text-gray-800 mb-2 px-4">
            Password:
        </label>
                <input
                    className="bg-gray-200 shadow border-blue-500 border rounded py-2 px-2 text-gray-700"
                    id="password" type="password" placeholder="******************"
                    value={this.state.password}
                    onChange={this.handlePassChange}>
                </input>
        </div>

            <div className="space-y-10"><br></br></div>
            {/*When user clicks "Sign in", make api call*/}
               <button
                   class="shadow transition duration-500 ease-in-out bg-blue-500 hover:bg-red-500 transform hover:-translate-y-1 hover:scale-105 bg-blue-300 border-blue-350 border-opacity-50 rounded-lg shadow-xl mx-32 px-10 py-3 rounded spacing-y-3 spacing-x-10 text-xl font-bold"
                   id="login-btn" type="button"
                   onClick={() => this.loginFxn()}>
                   Sign in
               </button>

             <div className="space-y-10"><br></br></div>

                </form>

            </div></span></div></div></div>
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
                style={{
                    position: 'absolute',
                    right: 40,
                    top: -18,
                }}
                className="bg-red-500 text-white hover:bg-red-700 font-bold w-32 rounded px-4 py-2 mt-6 align-right"
                id="logout-btn" type="button"
                onClick={() => this.logoutFxn()}>
                Sign out?
            </button>

            <div class="rounded rounded-t-lg border-2 bg-gray-200 card shadow w-1/3 mx-64 items-center h-full justify-center mt-24 pb-3">
                <h1 class="text-center px-3 pb-6 pt-2"> Hey {this.state.username}! </h1>

                <div className="flex justify-center pb-3 text-grey-dark">
                    <div className="text-center mr-3 border-r pr-3">
                        <h2> {this.state.user_rank}</h2>
                        <span> Rank </span>
                    </div>
                Points: { this.state.user_points }
            </div>
            </div>
        </div>)
    }




    //api call to get user's rank and points
    profileAPICall = async () => {

        const cookies = new Cookies()

        //store user input in FormData format
        let apiData = new FormData()
        apiData.append("user_id", cookies.get('username'))
        apiData.append("token", cookies.get('token'))

        //api call parameters
        let requestOptions = {
            method: 'POST',
            body: apiData,
            redirect: 'follow'
        };

        //make api call
        let fetch_url = url + "profile_page/api/profile"
        let response = await fetch(fetch_url, requestOptions)

        //make sure api call was successful, display error message if not
        if (!response.ok) {
            Swal.fire({
                title: 'User profile not found!',
                icon: 'error',
                text: "Please make sure you're signed in"
            })
            return
        }

        //otherwise, jsonify the api return
        let returned = await response.json()
        this.setState({ user_points: returned["user_profile"]["points"],
                             user_rank: returned["user_profile"]["rank"]})
    }

    render() {

        //display login screen if not logged in
        const cookies = new Cookies()
        if ((this.state.loggedIn === false) || (cookies.get('token') === '')){
            return (this.displayLogIn())
        }

        //display user profile page with option to log out
        else {
            this.profileAPICall()
            return(this.displayUserProfile())
        }
    }
}
export default Profile