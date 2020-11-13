import React, {Component} from 'react'
import Swal from "sweetalert2"

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

        //store the username and password that a user types in
        this.state = {
            username: null,
            password: null
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

        //store user input in FormData format
        let user_and_pass = new FormData()
        user_and_pass.append("user_id", this.state.username)
        user_and_pass.append("password", this.state.password)

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
                        Login to view your profile!
                    </h1>

                    {/*Username and password boxes*/}
                    <div class="align-center items-center">
                        <label class="text-xl ml-32 px-4">
                            Username:
                        </label>
                        <input class="bg-gray-200 shadow border-blue-500 border rounded w-48 py-2 px-2 text-gray-700"
                               id="username" type="text" value={this.state.username}
                               onChange={this.handleUserChange}>
                        </input>
                        <div class="py-4 px-3">
                        <label className="text-xl ml-32 px-3">
                            Password:
                        </label>
                        <input className="bg-gray-200 shadow border-blue-500 border rounded w-48 py-2 px-2 text-gray-700"
                               id="password" type="password" placeholder="******************" value = {this.state.password}
                               onChange={this.handlePassChange}>
                        </input>
                        </div>
                    </div>

                    {/*When user clicks "Sign in", make api call*/}
                    <button class="bg-blue-500 text-white hover:bg-blue-700 ml-64 font-bold rounded py-2 px-4" id="login-btn" type="button"
                        onClick={() => this.loginFxn()}>
                        Sign in
                    </button>
                </div>
            </form>
        )
    }
}
export default Profile