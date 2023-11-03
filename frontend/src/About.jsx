function About({ onClose }) {
    return (
        <div className="about-section">
            <h4>Where do the numbers come from?</h4>
            <p>In a typical local election, there are no polls to draw from to guess electoral outcomes. That means that you have to use your own knowledge and intuition to assign these numbers. Given that school board elections have become more polarized, you can make an educated guess on how likely a Democratic, Independent or Republican voter would select a specific candidate.</p>
            <h4>How are the electorate numbers determined?</h4>
            <p>It's a rough guess based on measuring how many voted for both a popular Democrat and a popular Republican, and vice versa. The electorate shifts every election, but these numbers use the 2020 presidential election to estimate the electorate.</p>
            <h4>How is the website programmed?</h4>
            <p>The election predicting engine is written in Python, while the frontend website display is written in React. All source code is available on Github and reporting technical issues is encouraged.</p>
            {/* Add a close button */}
            <button onClick={onClose}>Close window</button>
        </div>
    );
}

export default About;
