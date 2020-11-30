import React, { Component } from 'react'
import Swal from "sweetalert2"
import Cookies from "universal-cookie"
import Particles from "react-particles-js"

//Fix XSS security issues when developing locally
//this allows us to test separately locally and on Heroku by changing just one line
const local = "http://127.0.0.1:8000/";
const reactLocal = "http://localhost:3000/"
const remote = "https://data-structures-game.herokuapp.com/";
const tableHeaders = ["Game", "Type", "Difficulty", "Actions"]

//can also be const url = local; or const url = reactLocal;
const url = local;

/* This class provides the functionality for logging in and out,
   registering a new account and (eventually) adding friends
   and viewing user's profile info
 */

const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}

class Profile extends Component {
    constructor(props) {
        super(props);

        //see if logged in when profile page called
        const cookies = new Cookies();
        let prevLogin //for checking if logged in already, true if already logged in
        if ((cookies.get('token')) && (cookies.get('token') != '')) {
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
            user_name: null,
            user_points: null,
            user_rank: null,
            user_games: null,
            show_profile: false,
            auth_error: false,
        }
    }


    //api call to login
    //Note: api uses FormData for this call
    loginFxn = async () => {

        //if either field is blank, prompt user for input
        if (!this.state.username || !this.state.password) {
            Swal.fire("Please fill in both the username and password fields")
            return
        }

        //hash password
        let CryptoJS = require("crypto-js")

        //use username as salt for SHA-256 hash, so combine username and plaintext pw into one string
        let toHash = this.state.username + this.state.password
        this.setState({ password: "" })

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
            cookies.set('username', this.state.username, { path: '/' })

            //update state to reflect successful login
            this.setState({ loggedIn: true })

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
        if (returned["status"] == "success") {

            //remove cookies and set to empty to double-check
            cookies.remove('username', { path: '/' })
            cookies.remove('token', { path: '/' })
            cookies.set('username', '', { path: '/' })
            cookies.set('token', '', { path: '/' })

            this.setState({ loggedIn: false })

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
                                        className="shadow transition duration-500 ease-in-out bg-blue-500 hover:bg-red-500 transform hover:-translate-y-1 hover:scale-105 bg-blue-300 border-blue-350 border-opacity-50 rounded-lg shadow-xl mx-32 px-10 py-3 rounded spacing-y-3 spacing-x-10 text-xl font-bold"
                                        id="login-btn" type="button"
                                        onClick={() => this.loginFxn()}>
                                        Sign in
                                    </button>
                                    <div className="space-y-10"><br></br></div>

                                </form>

                            </div></span></div></div></div>
        )
    }

    authError = () => {
        Swal.fire({
            title: 'User profile not found!',
            icon: 'error',
            text: "Make sure you're logged in",
            confirmButtonText: 'Return to Home Page'

            //return to home page if click on button
        }).then((result) => {

            //if player clicks "Return to Home Page" button, redirect there
            if (result.isConfirmed) {
                window.location.href = "/"
            }
        })
    }

    viewCallback = (id) => {
        //store user input in FormData format
        let apiData = new FormData()
        apiData.append("user_id", this.state.user_name)
        apiData.append("game_id", id)
        apiData.append("token", this.state.token)

        //api call parameters
        let requestOptions = {
            method: 'POST',
            body: apiData,
            redirect: 'follow'
        };

        // //make api call
        // let fetch_url = url + "profile_page/api/load_board"
        // let response = await fetch(fetch_url, requestOptions)

        Swal.fire({
            title: 'Failed to load game!',
            icon: 'error',
            text: "This feature is under development."
            })
        }


    shareCallbackHelper = async (id, dest_user) => {
    
        const cookies = new Cookies()

        //store user input in FormData format
        let apiData = new FormData()
        apiData.append("source_user_id", cookies.get('username'))
        apiData.append("game_id", id)
        apiData.append("dest_user_id", dest_user)
        apiData.append("token", cookies.get('token'))

        //api call parameters
        let requestOptions = {
            method: 'POST',
            body: apiData,
            redirect: 'follow'
        };

        //make api call
        let fetch_url = url + "profile_page/api/share"
        let response = await fetch(fetch_url, requestOptions)
        return (response.ok)
    }    

    shareCallback = (id) => {
        Swal.fire({
            title: "Who would you like to share with?",
            input: 'text',
            inputAttributes: {
              autocapitalize: 'off'
            },
            showCancelButton: true,
            confirmButtonText: 'Share',
            showLoaderOnConfirm: true,
            preConfirm: (dest_user) => {}
        }).then((result) => {
            if (result.isConfirmed) {

                if (result.value === "") {
                    Swal.fire({
                        title: 'Failed to share game!',
                        icon: 'error',
                        text: "You need to input something!"
                    })
                } else {
                    //make api call
                    let ok = this.shareCallbackHelper(id, result.value);
                    if (!ok) {
                        Swal.fire({
                            title: 'Failed to share game!',
                            icon: 'error',
                            text: "Try again later."
                        })
                    } else {
                        Swal.fire(
                            'Shared!',
                            'Your game has been shared.',
                            'success'
                        )
                    }
                }
            }
        })
    }


    deleteCallbackHelper = async (id) => {
        
        const cookies = new Cookies()

        //store user input in FormData format
        let apiData = new FormData()
        apiData.append("user_id", cookies.get('username'))
        apiData.append("game_id", id)
        apiData.append("token", cookies.get('token'))

        //api call parameters
        let requestOptions = {
            method: 'POST',
            body: apiData,
            redirect: 'follow'
        };

        //make api call
        let fetch_url = url + "profile_page/api/delete_board"
        let response = await fetch(fetch_url, requestOptions)
        return (response.ok === true)
    }

    deleteCallback = (id) => {
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {

                //make api call
                let ok = this.deleteCallbackHelper(id);
                if (!ok) {
                    Swal.fire({
                        title: 'Failed to delete game!',
                        icon: 'error',
                        text: "Try again later."
                    })
                } else {
                    Swal.fire(
                        'Deleted!',
                        'Your file has been deleted.',
                        'success'
                    )
                    this.requestProfileUpdate()
                }
            }
        })
    }

    // The function below will accept a single game and its index to add it to the table
    appendGame = (singleGame) => {

        let blueButtonStyle = "text-grey-lighter font-bold py-1 px-3 mx-1 rounded text-xs bg-blue hover:bg-blue-dark"
        let redButtonStyle = "text-grey-lighter font-bold py-1 px-3 mx-1 space-x-4 rounded text-xs bg-red hover:bg-red-dark"

        return (
            <tr>
                <td className="py-4 px-6 border-b border-grey-light"> {singleGame.game_id.substring(0, 8)}</td>
                <td className="py-4 px-6 border-b border-grey-light"> {singleGame.curr_data_structure}</td>
                <td className="py-4 px-6 border-b border-grey-light"> {singleGame.difficulty}</td>
                <td className="flex space-x-4 py-4 px-6 border-b border-grey-light">
                    <button className={blueButtonStyle} onClick={() => this.viewCallback(singleGame.game_id)}> View </button>
                    <button className={blueButtonStyle} onClick={() => this.shareCallback(singleGame.game_id)}> Share </button>
                    <button className={redButtonStyle} onClick={() => this.deleteCallback(singleGame.game_id)}> Delete </button>
                </td>
            </tr>
        )
    }

    buildGamesHeader = (col_name) => {
        return (<th className="py-4 px-6 bg-grey-lightest font-bold uppercase text-sm text-grey-dark border-b border-grey-light">
            {col_name}
        </th>)
    }

    buildGames = (games) => {
        if (games == null || games.length == 0) {
            return <div></div>;
        } else {

            let header = []
            tableHeaders.forEach(header_col => {
                header.push(this.buildGamesHeader(header_col));
            })

            let game_rows = []
            for (const game of games) {
                game_rows.push(this.appendGame(game))  // Creates and appends each row to the table body
            }

            return (
                <table className="text-left w-full border-collapse bg-white shadow-2xl rounded my-6">
                    <thead> {header} </thead>
                    <tbody> {game_rows} </tbody>
                </table>)
        }
    }


    //display user profile and sign out button
    displayUserProfile = () => {

        return (<div>
            
             <link href="https://unpkg.com/tailwindcss@0.3.0/dist/tailwind.min.css" rel="stylesheet"></link> {/* link to stylesheet for profile */}
            {/*When user clicks "Sign out", make api call to log out*/}
            <button
                style={{
                    position: 'absolute',
                    right: 50,
                    top: -5,
                }}
                className="bg-red-500 text-white hover:bg-red-700 font-bold w-32 rounded px-4 py-2 mt-6 align-right"
                id="logout-btn" type="button"
                onClick={() => this.logoutFxn()}>
                Sign out?
                </button>

            <div class="flex h-screen items-center justify-center">
                <div class="grid grid-flow-row auto-rows-max">
                    <div class="bg-white shadow-2xl rounded rounded-t-lg overflow-hidden shadow max-w-md my-3">
                        <img src="/static/bamboo-forest.jpg" class="w-full" />
                        <div class="flex justify-center -mt-8">
                            <img src="/static/bohemian_panda.png" class="rounded-full border-solid border-white border-2 -mt-3 h-32 w-32" />
                        </div>
                        <div class="text-center px-3 pb-6 pt-2">
                            <h3 class="text-black text-md bold font-bold">{this.state.user_name}</h3>
                        </div>
                        <div class="flex justify-center pb-3 text-grey-dark">
                            <div class="text-center mr-3 border-r pr-3">
                                <h2 className="space-y-5 text-md text-center font-semibold text-gray-800 mb-2">{this.state.user_points}</h2>
                                <span>Total Points</span>
                            </div>
                            <div class="text-center">
                                <h2 className="space-y-5 text-md text-center font-semibold text-gray-800 mb-2">{this.state.user_rank}</h2>
                                <span>Ranking</span>
                            </div>
                        </div>
                    </div>
                    {this.buildGames(this.state.user_games)}
                </div>
            </div>
        </div>)

    }

    // confirm profile is ready to show
    loadProfile = () => {
        this.setState({ show_profile: true})
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
        return response;
    }

    // set state based off of API success
    updateProfile = async () => {
        
        // call to API
        let response = this.profileAPICall()
        
        // check if response fails
        if(!response.ok) {
            this.setState({
                auth_error: true},
                () => { this.loadProfile();
            })

        // api call good, save user profile info
        } else {
            let returned = await response.json()
            this.setState({
                auth_error: false,
                user_games: returned["user_profile"]["saved_games"],
                user_name: returned["user_profile"]["user_name"],
                user_points: returned["user_profile"]["points"],
                user_rank: returned["user_profile"]["rank"]},
                () => { this.loadProfile();
            })
        }
    }

    // a change has been made, update profile
    requestProfileUpdate = () => {
        this.setState({ show_profile: false}, () => {this.updateProfile();})
    }


    render() {

        //display login screen if not logged in
        const cookies = new Cookies()
        if ((this.state.loggedIn === false) || (cookies.get('token') === '')) {
            return (this.displayLogIn())
        }

        //display user profile page with option to log out
        else {
            if(this.state.show_profile) {
                if (this.auth_error) {
                    return(
                      <div>
                        {this.authError()}
                      </div>)
                } else {
                    return (this.displayUserProfile())
                }

            // display loading screen while user waits
            } else {
                return ( 
                    <div>
                      <link rel="stylesheet" href="https://pagecdn.io/lib/font-awesome/5.10.0-11/css/all.min.css"></link>
                      <div className="w-full h-full fixed block top-0 left-0 bg-white opacity-75 z-50">
                        <span
                          style={{top: '50%'}} 
                          className="text-blue-400 opacity-75 top-1/2 my-0 mx-auto block relative w-0 h-0">
                          <i className="fas fa-circle-notch fa-spin fa-5x"></i>
                        </span>
                      </div>
                    </div>)                
            }
        }
    }
}
export default Profile