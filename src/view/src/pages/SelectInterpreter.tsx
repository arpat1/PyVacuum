import React, { useState } from "react"
import styles from "./SelectInterpreter.module.css"
import filesvg from "../shared/file_icon.svg"
import { eel } from "../App"

const SelectInterpreter = () => {
    const [fileNames, setFileNames] = useState<string[]>([])
    const [selectedFile, setSelectedFile] = useState("")
    const [selectedInterpreter, setSelectedInterpreter] = useState("")

    const handleSelectedFileChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedFile(e.target.value)
        e.preventDefault()
    }

    const selectFiles = (e: React.MouseEvent<HTMLAnchorElement>) => {
        eel.select_files()((paths: Array<string>) => {
            const newFiles = paths
            .map(p => p.split("/").at(-1))
            .filter(p => typeof p == "string")

            const newFileNames = [...new Set([...fileNames, ...newFiles])]
            setFileNames(newFileNames)
            setSelectedFile(newFileNames[0])
        })
        createRipples(e)
    }

    const selectInterpreter = (e: React.MouseEvent<HTMLAnchorElement>) => {
        eel.select_interpreter()((interpreter: string) => setSelectedInterpreter(interpreter))
        createRipples(e)
    }

    const runInterpreter = (e: React.MouseEvent<HTMLAnchorElement>) => {
        if (selectedInterpreter && selectedFile){
            eel.run_file(selectedFile)
        } else if (!selectedInterpreter) {
            alert("First select interpreter!")
        } else if (!selectedFile) {
            alert("First select python file!")
        }
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