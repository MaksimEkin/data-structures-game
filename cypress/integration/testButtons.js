context('Home Page Testing', () => {
    beforeEach(() => {
    cy.visit('http://127.0.0.1:8000/')
})

    //test typing player names into the playerList DOM element
    it('Type text into Players correctly', () => {
        cy.get('input[name=playerList]')

            //clear the field, so it should be empty (not say "ID1")
            .clear().should('have.value', '')

            //type player names in, separated by comma
            .type("Player A, Player B").should('have.value', 'Player A, Player B')
    })

})

