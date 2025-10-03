import React from "react"
import styles from "./SelectInterpreter.module.css"

const SelectInterpreter = () => {
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
        </div>
    )
}

export default SelectInterpreter