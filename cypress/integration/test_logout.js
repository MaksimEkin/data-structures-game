context('Logout Testing', () => {
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

   //login & verify logout takes you back to login page
    it("Test Username on User Profile", () => {
        cy.get("input[id=username]")
            .type('user1').should('have.value', 'user1')
        cy.get("input[id=password")
            .type('pass1').should('have.value', 'pass1')
        cy.contains('Sign in').click()

        //logout, verify correct popup, and that no longer on user profile page
        cy.contains('Sign out').click()
        cy.contains('table').should('not.exist')

        //verify that back at login page
        cy.get("input[id=username]")
    })

})