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

    //logging out before logging in should fail
    it('Logout without logging in', () => {
        cy.contains('Sign out').click()
    })

})