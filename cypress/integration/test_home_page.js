context('Home Page Testing', () => {
    const local = "http://127.0.0.1:8000/";
    const reactLocal = "http://localhost:3000/";
    const remote = "https://data-structures-game.herokuapp.com/";

    const url = local;
    beforeEach(() => {
    cy.visit(url)
})

    //start game option redirects to correct URL
    it('Pressing start game redirects to correct url', () => {
        cy.contains('Start Game').click()
        cy.url().should('contain', '/game_board')
    })

    //clicking "Home" should keep url the same
    it('Testing Home URL', () => {
        cy.contains('Home').click()
        cy.url().should('eq', url)
    })

    //test typing player names into the playerList DOM element
    it('Type text into Players correctly', () => {
        cy.get('input[name=playerList]')

            //clear the field, so it should be empty (not say "ID1")
            .clear().should('have.value', '')

            //type player names in, separated by comma
            .type("Player A, Player B").should('have.value', 'Player A, Player B')
    })

    //test selecting levels
    it('Level correct?', () => {
        cy.get('#level_select').select('Easy').should('have.value', 'Easy')
        cy.get('#level_select').select('Medium').should('have.value', 'Medium')
        cy.get('#level_select').select('Hard').should('have.value', 'Hard')
    })

})

