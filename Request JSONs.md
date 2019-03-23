### Organization signup:

let payload = {
                'name': this.state.name,
                'contact_email': this.state.email,
                'address_line_1': this.state.address_line_1,
                'address_line_2': this.state.address_line_2,
                'city':this.state.city,
                'state':this.state.state,
                'country':this.state.country,
                'zip':this.state.zip,
                'phone':this.state.phone,
                'headquarter' : this.state.headquarter,
                'founded_date'  : this.state.founded_date,
                'organization_type': this.state.organization_type
            };
            
#### API  :-> /user/signup

export const doSignUp = (payload) =>
    fetch (`/user/signup`,
        {
            method: 'POST',
            headers: {
                ...headers,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        }).then(res => {
        return res;
    }).catch(error => {
        console.log("Error: ");
        console.log(error);
        return error;
    });
   
Response:
200 -> signup request successfully submitted
(code) -> when email already exitsxt and user cannot sign up
(code) -> some error occurred

### Login

let payload = {
                'email': this.state.email,
                'password': this.state.password
            };
           
export const doLogin = (payload) =>
    fetch(`/user/login`, {
        method: 'POST',
        headers: {
            ...headers,
            'Content-Type': 'application/json'
        },
        credentials:'include',
        body: JSON.stringify(payload)
    }).then(res => {
        return res;
    }).catch(error => {
        console.log("This is error");
        console.log(error);
        return error;
    });
    
Response:
200 -> sucessfully signed in 
user's profile data and session
(code) -> invalid username and password
(code) -> any other error       

### Organization user sends data to be added to the block.

let payload = {
                'user_email' : this.state.email,
                'role' : this.state.role,
                'start_date' : this.state.start_date,
                'end_date' : this.state.end_date,
                'highlights' : this.state.highlights
            };
            
            
