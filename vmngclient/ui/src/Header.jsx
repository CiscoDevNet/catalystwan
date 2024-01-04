import React from 'react';
import Image from 'next/image'

const Header = () => {
    return (
        <header style={{height: '120px',}}>
            <Image src="/images/CiscoLogoWhite.png" width={200} height={200} />
        </header>
    );
};

export default Header;
