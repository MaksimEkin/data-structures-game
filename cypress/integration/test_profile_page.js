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

    //test successful login with username "user1" and password "pass1"
    it("Test Successful Login", () => {
        cy.get("input[id=username]")
            .type('user1').should('have.value', 'user1')
        cy.get("input[id=password")
            .type('pass1').should('have.value', 'pass1')
        cy.contains('Sign in').click()

        //make sure logout button appears, to verify reached profile page
        cy.get('#logout-btn').should('contain', 'out')
    })

    //test that username on profile is correct (user1)
    it("Test Username on User Profile", () => {
        cy.get("input[id=username]")
            .type('user1').should('have.value', 'user1')
        cy.get("input[id=password")
            .type('pass1').should('have.value', 'pass1')
        cy.contains('Sign in').click()

        //make sure username displayed on profile is right
        cy.contains('user1')

        //incorrect username should NOT be on profile page
        cy.contains('user2').should('not.exist')
    })

    //verify that all elements of page are present
    it("Profile Page Elements Found?", () => {
        cy.get("input[id=username]")
            .type('user1').should('have.value', 'user1')
        cy.get("input[id=password")
            .type('pass1').should('have.value', 'pass1')
        cy.contains('Sign in').click()

        //check for presence of points, ranking & table of games
        cy.contains('Total Points')
        cy.contains('Ranking')
        cy.get('th')
        cy.get('td')
    })

    //see if "View game" popup appears
    it("Test View Game", () => {
        cy.get("input[id=username]")
            .type('user1').should('have.value', 'user1')
        cy.get("input[id=password")
            .type('pass1').should('have.value', 'pass1')
        cy.contains('Sign in').click()

        //click button, manually verify "under construction" popup
        cy.contains("View").click()
    })

    //test that sharing works
    it("Test Share Button brings up popup", () => {
        cy.get("input[id=username]")
            .type('user1').should('have.value', 'user1')
        cy.get("input[id=password")
            .type('pass1').should('have.value', 'pass1')
        cy.contains('Sign in').click()

        //can't access text box to actually check sharing works
        cy.contains("Share").click()
    })

    //test delete button
    it("Test Delete Button brings right pop up", () => {
        cy.get("input[id=username]")
            .type('user1').should('have.value', 'user1')
        cy.get("input[id=password")
            .type('pass1').should('have.value', 'pass1')
        cy.contains('Sign in').click()

        //check that right popups occur
        cy.contains("Delete").click()
    })

})