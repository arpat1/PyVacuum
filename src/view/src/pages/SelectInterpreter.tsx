import React, { useState } from "react"
import styles from "./SelectInterpreter.module.css"
import filesvg from "../shared/file_icon.svg"

const SelectInterpreter = () => {
    const [fileNames, setFileNames] = useState(["file1.py", "file2.py", "file3.py"])
    const createRipples = (e: React.MouseEvent<HTMLAnchorElement>) => {
        const el = e.currentTarget
        const ripples = document.createElement("span")
        let posx = e.clientX - e.currentTarget.offsetLeft
        let posy = e.clientY - e.currentTarget.offsetTop

        ripples.style.left = posx + "px"
        ripples.style.top = posy + "px"

        el.appendChild(ripples)

        setTimeout(() => {
            ripples.remove()
        }, 1000)
    }
    return (
        <div className={styles.container}>
            <a href="#" className={styles["select-ripple-btn"]} onClick={createRipples}>
                Select files to run
            </a>
            <a href="#" className={styles["select-ripple-btn"]} onClick={createRipples}>
                Select interpreter
            </a>
            <label>Choose file:</label>
            <select className={styles["custom-select"]}>
                {fileNames.length ? 
                fileNames.map((fileName) => 
                <option value={fileName} key={fileName}>
                    <img src={filesvg}/>
                    {fileName}
                </option>
                ) 
                : 
                <option value="first choose files">first choose files</option>}
            </select>
        </div>
    )
}

export default SelectInterpreter