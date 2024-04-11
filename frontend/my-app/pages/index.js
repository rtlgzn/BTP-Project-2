import React from 'react';
import { Row, Col, Image } from 'react-bootstrap';

//Home page - display home page contents
const Home = () => {
    return (
        <>
            <Image src="https://media.timeout.com/images/105239239/image.jpg" fluid rounded />
            <Row style={{marginTop: '15px'}}>
                <Col md={6}>
                    <p>
                    Nestled in the heart of a bustling urban landscape, our restaurant, named Gastronomique Haven, offers an enchanting escape for culinary enthusiasts seeking an unforgettable dining experience. Step into our warmly lit interior adorned with modern décor and earthy tones, creating an ambiance of refined elegance.
                    </p>
                    <p>
                    The aroma of expertly crafted dishes wafts through the air, enticing patrons to indulge in a symphony of flavors meticulously prepared by our passionate chefs. From the freshest locally sourced ingredients to exotic spices from distant lands, every dish on our diverse menu tells a story of culinary mastery and innovation.                    </p>
                </Col>
                <Col md={6}>
                    <p>
                    Whether youre savoring a succulent steak cooked to perfection, delighting in the vibrant colors of a seasonal salad, or indulging in a decadent dessert, each bite promises to tantalize the senses and leave a lasting impression. With impeccable service and an extensive wine list curated to complement every palate, Gastronomique Haven is not just a restaurant; its a destination where food becomes art and dining becomes an experience to cherish.                    </p>
                </Col>
            </Row>
        </>
    );
};

export default Home;