import React, {Component} from 'react'

class Profile extends Component {
    constructor(props) {
        super(props);
    }

    loginFxn = () => {

    }

    render() {
        return (
            <form class="container mx-auto h-full flex justify-center items-center align-center">
                <div class="w-1/2 font-hairline">
                    <h1 class="mt-12 mb-6 text-3xl text-center">Login to view your profile!</h1>
                    <div>
                        <label class="text-xl ml-32"> Username: </label>
                        <input class="bg-blue-100 shadow border rounded w-1/3 py-2 px-3 text-gray-700" id="username" type="text"></input>
                    </div>
                    <div class="py-4 px-3">
                        <label className="text-xl ml-32"> Password: </label>
                        <input className="bg-blue-100 shadow border rounded w-1/3 py-2 px-3 text-gray-700" id="password" type="text"></input>
                    </div>
                    <button class="bg-blue-500 text-white hover:bg-blue-700 ml-64 font-bold rounded py-2 px-4" id="login-btn" type="button" >
                        Sign in
                    </button>
                </div>
            </form>
        )
    }
}
export default Profile