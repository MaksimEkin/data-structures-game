//Note: Cypress does not easily support sweetalert testing
//manually checked that correct pop up appeared

context('Login Page Testing', () => {
    const local = "http://127.0.0.1:8000/";
    const reactLocal = "http://localhost:3000/";
    const remote = "https://data-structures-game.herokuapp.com/";

    const url = local;

    //visit profile page
    beforeEach(() => {
        cy.visit(url)
        cy.get('nav').click()
        cy.contains('Profile').click()
    })

    //see if when click on profile page, redirect to correct url
    it('successfully reach profile page', () => {
        cy.url().should('contain', '/profile_page')
    })

    //test successful login with username "useruser" and password "pass1"
    it("Test Successful Login", () => {
        cy.get("input[id=username]")
            .type('user1').should('have.value', 'user1')
        cy.get("input[id=password")
            .type('pass1').should('have.value', 'pass1')
        cy.contains('Sign in').click()
    })

    //test attempt to log in without filling in both username and password
    it("Leave both options blank", () => {
        cy.get("input[id=username]").clear().should('have.value', '')
        cy.get("input[id=password").clear().should('have.value', '')
        cy.contains('Sign in').click()
    })

    //leave username blank
    it("Leave just username blank", () => {
        cy.get("input[id=username]").clear().should('have.value', '')
        cy.get("input[id=password").type('password').should('have.value', 'password')
        cy.contains('Sign in').click()
    })

    //leave password blank
    it("Leave just password blank", () => {
        cy.get("input[id=username]").type('user').should('have.value', 'user')
        cy.get("input[id=password").clear().should('have.value', '')
        cy.contains('Sign in').click()
    })

    //incorrect login
    it("Failing login", () => {
        cy.get("input[id=username]").type('use').should('have.value', 'use')
        cy.get("input[id=password").type('use').should('have.value', 'use')
        cy.contains('Sign in').click()
    })

})