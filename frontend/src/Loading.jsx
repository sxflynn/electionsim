import './loading.css';

function Loading(){
    return (
        <div className="lds-spinner">
        <div></div><div></div><div></div><div></div><div></div>
        <div></div><div></div><div></div><div></div><div></div>
        <div></div><div></div>
      </div>
    );
}

export default Loading;