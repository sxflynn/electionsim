// randomizeUtils.js

export const randomizeData = (configData, setData, setIsEdited) => {
    // Generate randomized electorate data such that they sum up to 1
    let rep = Math.random();
    let ind = Math.random();
    let dem = 1 - rep - ind;
    while (dem < 0 || dem > 1) { // Ensure the sum is 1 and each is between 0 and 1
        rep = Math.random();
        ind = Math.random();
        dem = 1 - rep - ind;
    }

    rep = Math.round(rep * 100) / 100;
    ind = Math.round(ind * 100) / 100;
    dem = Math.round(dem * 100) / 100;

    const randomizedElectorate = {
        "Republicans": rep,
        "Independents": ind,
        "Democrats": dem
    };

    // Generate randomized voter profile data
    const randomizedVoterProfiles = {};
    for (const party of Object.keys(configData.voterProfiles)) {
        randomizedVoterProfiles[party] = {};
        for (const candidate of configData.candidates) {
            const randomValue = 0.01 + Math.random() * 0.98;
            randomizedVoterProfiles[party][candidate] = Math.round(randomValue * 100) / 100;
        }
    }

    setData(prevData => ({
        ...prevData,
        electorate: randomizedElectorate,
        voterProfiles: randomizedVoterProfiles
    }));

    setIsEdited(true);
    console.log("Edited set to true");
}
