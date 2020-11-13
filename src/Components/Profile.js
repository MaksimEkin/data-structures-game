import React, {Component} from 'react'

//Fix XSS security issues when developing locally
//this allows us to test separately locally and on Heroku by changing just one line
const local = "http://127.0.0.1:8000/";
const reactLocal = "http://localhost:3000/"
const remote = "https://data-structures-game.herokuapp.com/";

//can also be const url = local; or const url = reactLocal;
const url = local;

class Profile extends Component {
    constructor(props) {
        super(props);

        this.state = {
            username: null,
            password: null
        }
    }

    loginFxn = async () => {
        let user_and_pass = new FormData()
        user_and_pass.append("user_id", "useruser")
        user_and_pass.append("password", "pass1")
        let requestOptions = {
            method: 'POST',
            body: user_and_pass,
            redirect: 'follow'
        };

        let fetch_url = url + "profile_page/api/login"
        let response = await fetch(fetch_url, requestOptions);
        let returned = await response.json();

        if (returned["status"] == "success"){
            console.log("successfully logged in")
        }
    }

    handleUserChange = (event) => {
        this.setState({
            username: event.target.value
        })
    }

    handlePassChange = (event) => {
        this.setState({
            password: event.target.value
        })
    }

    render() {
        return (
            <form class="container mx-auto h-full flex justify-center items-center align-center">
                <div class="w-1/2 font-thin">
                    <h1 class="mt-12 mb-6 text-3xl text-center">
                        Login to view your profile!
                    </h1>

                    <div>
                        <label class="text-xl ml-32">
                            Username:
                        </label>
                        <input class="bg-gray-200 shadow border-blue-500 border rounded w-1/3 py-2 px-3 text-gray-700"
                               id="username" type="text" value={this.state.username}
                               onChange={this.handleUserChange}>
                        </input>
                    </div>
                    <div class="py-4 px-3">
                        <label className="text-xl ml-32">
                            Password:
                        </label>
                        <input className="bg-gray-200 shadow border-blue-500 border rounded w-1/3 py-2 px-3 text-gray-700"
                               id="password" type="text" value = {this.state.password}
                               onChange={this.handlePassChange}>
                        </input>
                    </div>

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