import React, { createContext } from 'react'

export const GlobalContext = createContext({
    matrixUserId: "",
    setMatrixUserId: () => {},
    githubUserId: "",
    setGithubUserId: () => {}
});
