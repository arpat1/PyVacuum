import React, { useState } from "react"
import styles from "./SelectInterpreter.module.css"
import filesvg from "../shared/file_icon.svg"

const SelectInterpreter = () => {
    const [fileNames, setFileNames] = useState(["file1.py", "file2.py", "file3.py"])
    const [selectedFile, setSelectedFile] = useState("")

    const handleSelectedFileChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedFile(e.target.value)
    }

    const selectFiles = (e: React.MouseEvent<HTMLAnchorElement>) => {
        //call python function to select files
        createRipples(e)
    }

    const selectInterpreter = (e: React.MouseEvent<HTMLAnchorElement>) => {
        //call python function to select interpreter
        createRipples(e)
    }

    const runInterpreter = (e: React.MouseEvent<HTMLAnchorElement>) => {
        //call python function to run interpreter
        createRipples(e)
    }

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
            <a href="#" className={styles["select-ripple-btn"]} onClick={selectFiles}>
                select files to run
            </a>
            <a href="#" className={styles["select-ripple-btn"]} onClick={selectInterpreter}>
                select interpreter
            </a>
            <label>choose file:</label>
            <select className={styles["custom-select"]} onChange={handleSelectedFileChange}>
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
            <a href="#" className={styles["select-ripple-btn"]} onClick={runInterpreter}>
                run!
            </a>
        </div>
    )
}

export default SelectInterpreter